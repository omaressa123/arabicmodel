import os
import math
from typing import List, Dict, Any
import torch
from datasets import load_dataset, DatasetDict
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    default_data_collator,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training


def build_prompt(sample: Dict[str, Any]) -> str:
    inp = sample.get("input", "").strip()
    topic = sample.get("topic", "").strip()
    formal = sample.get("formal", "").strip()
    parts = []
    if topic:
        parts.append(f"الموضوع: {topic}")
    if inp:
        parts.append(f"الطلب باللهجة المصرية: {inp}")
    if formal:
        parts.append(f"صياغة رسمية: {formal}")
    prompt = "\n".join(parts).strip()
    return prompt


def build_response(sample: Dict[str, Any]) -> str:
    slides = sample.get("slides", [])
    out_lines: List[str] = []
    for slide in slides:
        t = slide.get("title", "")
        if t:
            out_lines.append(f"# {t}")
        content = slide.get("content", [])
        for item in content:
            out_lines.append(f"- {item}")
        if t or content:
            out_lines.append("")
    response = "\n".join(out_lines).strip()
    return response


def format_text(sample: Dict[str, Any]) -> Dict[str, str]:
    instruction_header = "<|instruction|>\n"
    response_header = "\n<|response|>\n"
    prompt = build_prompt(sample)
    response = build_response(sample)
    full_prompt = instruction_header + prompt + response_header
    full_text = full_prompt + response
    return {"prompt_text": full_prompt, "response_text": response, "text": full_text}


def tokenize_examples(
    examples: Dict[str, List[str]],
    tokenizer: AutoTokenizer,
    max_length: int,
) -> Dict[str, List[List[int]]]:
    input_ids_list: List[List[int]] = []
    attention_masks: List[List[int]] = []
    labels_list: List[List[int]] = []
    prompts = examples["prompt_text"]
    responses = examples["response_text"]
    for p, r in zip(prompts, responses):
        tok_p = tokenizer(
            p,
            add_special_tokens=True,
            truncation=True,
            max_length=max_length,
        )
        tok_r = tokenizer(
            r,
            add_special_tokens=False,
            truncation=True,
            max_length=max_length,
        )
        ids = tok_p["input_ids"] + tok_r["input_ids"]
        ids = ids[:max_length]
        attn = [1] * len(ids)
        prompt_len = min(len(tok_p["input_ids"]), len(ids))
        labels = [-100] * prompt_len + ids[prompt_len:]
        if len(labels) < len(ids):
            labels += [-100] * (len(ids) - len(labels))
        if len(ids) < 2 or prompt_len >= len(ids):
            continue
        input_ids_list.append(ids)
        attention_masks.append(attn)
        labels_list.append(labels)
    return {"input_ids": input_ids_list, "attention_mask": attention_masks, "labels": labels_list}


def main():
    model_name = "mistralai/Mistral-7B-v0.1"
    data_file = os.path.join(os.path.dirname(__file__), "egyptian_presentation_dataset_batch1.json")
    max_length = 256
    bnb_dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float16
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=bnb_dtype,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        torch_dtype=bnb_dtype,
        device_map="auto",
    )
    model = prepare_model_for_kbit_training(model)
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    raw = load_dataset("json", data_files=data_file)
    ds: DatasetDict = raw["train"].train_test_split(test_size=0.05, seed=42)
    ds = ds.map(format_text, remove_columns=raw["train"].column_names)
    ds = ds.map(
        tokenize_examples,
        batched=True,
        fn_kwargs={"tokenizer": tokenizer, "max_length": max_length},
        remove_columns=["prompt_text", "response_text", "text"],
    )
    training_args = TrainingArguments(
        output_dir=os.path.join(os.path.dirname(__file__), "mistral-egyptian"),
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        num_train_epochs=3,
        logging_steps=10,
        save_steps=200,
        learning_rate=2e-4,
        fp16=(bnb_dtype == torch.float16),
        bf16=(bnb_dtype == torch.bfloat16),
        optim="paged_adamw_32bit",
        report_to="none",
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        save_total_limit=2,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ds["train"],
        eval_dataset=ds["test"],
        data_collator=default_data_collator,
    )
    model.config.use_cache = False
    trainer.train()
    trainer.save_model()
    try:
        model.push_to_hub("mistral-egyptian-lora", private=True)
        tokenizer.push_to_hub("mistral-egyptian-lora", private=True)
    except Exception:
        pass


if __name__ == "__main__":
    main()

