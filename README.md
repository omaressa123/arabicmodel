# 🎤 Arabic Voice-to-Presentation Generator (Offline AI System)

## 📌 Project Overview

This project is an **offline AI-powered system** that converts **Arabic (Egyptian dialect) voice input** into a **fully structured presentation (PowerPoint slides)**.

The system processes spoken Arabic, understands informal Egyptian dialect, and automatically generates professional slides with titles, bullet points, and optional speaker notes.

---

## 🎯 Objectives

* Convert Arabic speech into text (offline)
* Understand Egyptian dialect (colloquial Arabic)
* Transform informal input into structured formal content
* Generate presentation slides automatically
* Run fully offline without paid APIs

---

## 🧠 System Architecture

```
[User Voice Input 🎤]
        ↓
[Speech-to-Text Engine]
        ↓
[Text Preprocessing (Dialect Cleaning)]
        ↓
[Local AI Model (LLM)]
        ↓
[Slide Generator]
        ↓
[PowerPoint Output (.pptx)]
```

---

## 🧩 Technologies Used

### 🎤 Speech Recognition

* Whisper (offline speech-to-text)
* Supports Arabic and Egyptian dialect

### 🧠 Language Model (Offline)

* Local LLM via Ollama
* Models:

  * Mistral 7B
  * LLaMA 3
  * Phi-3

### 🔧 NLP Processing

* Rule-based text cleaning
* Dialect normalization (Egyptian → Formal Arabic)

### 📊 Presentation Generation

* python-pptx (PowerPoint file creation)

### 🌐 Backend (Optional)

* Flask (for web interface)

---

## ⚙️ System Workflow

### Step 1: Voice Input

User speaks in Egyptian Arabic:

> "اعمل برزنتيشن عن الذكاء الاصطناعي في الطب"

---

### Step 2: Speech-to-Text

Audio is converted into text using Whisper.

---

### Step 3: Text Cleaning

Remove slang and normalize text:

* "عاوز" → "أريد"
* "حاجة" → removed

---

### Step 4: AI Processing

Local LLM:

* Understands intent
* Extracts topic
* Generates structured slides

---

### Step 5: Slide Generation

Slides are created with:

* Title
* Bullet points
* Optional notes

---

### Step 6: Output

System generates:

* `.pptx` file (downloadable presentation)

---

## 🧪 Example

### Input (Voice → Text)

```
"اعمل برزنتيشن عن التسويق الرقمي وكده"
```

### Output

* Slide 1: Introduction to Digital Marketing
* Slide 2: أهمية التسويق الرقمي
* Slide 3: القنوات الرقمية
* Slide 4: استراتيجيات النجاح
* Slide 5: التحديات
* Slide 6: المستقبل

---

## 🧠 Dialect Handling Strategy

### 1. Rule-Based Normalization

Custom dictionary:

```python
{
  "عاوز": "أريد",
  "اعمل": "أنشئ",
  "حاجة": "",
  "وكده": ""
}
```

### 2. Preprocessing Pipeline

* Remove filler words
* Normalize verbs
* Clean repeated phrases

---

## 🔥 Features

* ✅ Fully offline (no API required)
* ✅ Supports Egyptian Arabic dialect
* ✅ Automatic slide generation
* ✅ Export to PowerPoint
* ✅ Modular architecture

---

## 🚀 Advanced Features (Future Work)

* 🎙️ Voice-controlled editing
* 🧠 Fine-tuned dialect model
* 🌐 Web interface with live preview
* 🖼️ Auto image generation
* 🎤 Slide narration (text-to-speech)

---

## ⚠️ Limitations

* Dialect understanding depends on dataset quality
* Local models are less accurate than cloud AI
* Requires moderate hardware (8–16GB RAM)

---

## 💻 System Requirements

| Component | Minimum  | Recommended  |
| --------- | -------- | ------------ |
| RAM       | 8GB      | 16GB         |
| CPU       | i5       | i7 / Ryzen 7 |
| GPU       | Optional | Recommended  |

---

## 🛠️ Installation

### 1. Install Whisper

```
pip install openai-whisper
```

### 2. Install Ollama

* Download from official website
* Run:

```
ollama run mistral
```

### 3. Install Dependencies

```
pip install python-pptx flask requests
```

---

## ▶️ How to Run

1. Start Ollama:

```bash
ollama serve
```

2. Run the generator with an audio file:

```bash
python main.py path/to/your/audio.wav
```

3. Find the generated presentation in the `output/` folder.

## 📂 Project Structure

```
arabicmodel/
│── main.py                 # Main entry point
│── verify_system.py        # Verification script
│── arabicmodel/
│   ├── config.py           # Configuration settings
│   ├── speech_to_text.py   # STT logic (Whisper)
│   ├── text_cleaning.py    # Dialect normalization
│   ├── slide_generator.py  # PowerPoint generation
│   └── requirements.txt    # Project dependencies
│── audio/                  # Input audio files
│── output/                 # Generated presentations
```

---

## 📊 Use Cases

* Students creating presentations quickly
* Business professionals generating slides
* Content creators
* Educational tools

---

## 🤝 Future Improvements

* Fine-tuned Egyptian dialect dataset
* Multi-language support
* Real-time voice streaming
* Integration with web platforms

---

## 📜 License

This project is open-source and free to use for educational purposes.

---

## 👨‍💻 Author

Developed as an AI + NLP + Speech Processing project for offline intelligent systems.

---
