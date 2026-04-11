import os
import json
import requests
import sys

# Ensure UTF-8 output for Arabic characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from arabicmodel.speech_to_text import ArabicSpeechToText
from arabicmodel.text_cleaning import preprocess_text
from arabicmodel.slide_generator import SlideGenerator
from arabicmodel.config import OLLAMA_API_URL, OLLAMA_SETTINGS, OUTPUT_DIR

class ArabicPresentationGenerator:
    def __init__(self):
        self.stt = ArabicSpeechToText()
        self.slide_gen = SlideGenerator()

    def generate_presentation_structure(self, topic_text):
        """Prompt the LLM to generate a structured presentation JSON."""
        prompt = f"""
        Generate a structured presentation in JSON format for the following topic: "{topic_text}".
        The presentation should be in Arabic. 
        Each slide should have a 'title' and a 'content' (a list of bullet points).
        The first slide should be a 'title' type slide with a 'title' and a 'subtitle'.
        
        Example JSON format:
        [
          {{"title": "عنوان البرزنتيشن", "subtitle": "الوصف الفرعي", "type": "title"}},
          {{"title": "المقدمة", "content": ["النقطة الأولى", "النقطة الثانية"]}},
          {{"title": "الخاتمة", "content": ["شكراً لكم"]}}
        ]
        
        ONLY return the JSON. No other text.
        """
        
        payload = {
            "model": OLLAMA_SETTINGS['model'],
            "prompt": prompt,
            "stream": False,
            "options": OLLAMA_SETTINGS['options']
        }
        
        try:
            print(f"Sending prompt to Ollama ({OLLAMA_API_URL})...")
            response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
            response.raise_for_status()
            response_json = response.json()
            
            # Extract and parse JSON from the LLM output
            llm_text = response_json.get('response', '').strip()
            print(f"Raw LLM Response: {llm_text}")
            
            # Simple way to find JSON in case the LLM adds extra text
            start = llm_text.find('[')
            end = llm_text.rfind(']') + 1
            if start != -1 and end != -1:
                json_str = llm_text[start:end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as je:
                    print(f"Failed to parse JSON segment: {je}")
                    print(f"Segment was: {json_str}")
                    return None
            else:
                print("Could not find valid JSON (missing brackets) in LLM response.")
                return None
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to Ollama. Is it running?")
            return None
        except Exception as e:
            print(f"Error communicating with Ollama: {e}")
            return None

    def run(self, audio_path, output_filename="presentation.pptx"):
        """Main flow: Audio -> STT -> Clean -> LLM -> PPTX"""
        print(f"Step 1: Transcribing audio from {audio_path}...")
        transcript = self.stt.transcribe(audio_path)
        print(f"Transcription: {transcript}")
        
        print("Step 2: Cleaning text and normalizing dialect...")
        cleaned_text = preprocess_text(transcript)
        print(f"Cleaned Topic: {cleaned_text}")
        
        print("Step 3: Generating presentation structure using Mistral (via Ollama)...")
        slides_data = self.generate_presentation_structure(cleaned_text)
        
        if not slides_data:
            print("Failed to generate presentation structure.")
            return None
            
        print("Step 4: Creating PowerPoint slides...")
        output_path = self.slide_gen.create_presentation(slides_data, output_filename)
        
        print(f"Success! Presentation saved at: {output_path}")
        return output_path

import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an Arabic presentation from a voice recording.")
    parser.add_argument("audio", help="Path to the audio file (.wav, .mp3, etc.)")
    parser.add_argument("--output", default="presentation.pptx", help="Name of the output presentation file.")
    
    args = parser.parse_args()
    
    generator = ArabicPresentationGenerator()
    try:
        generator.run(args.audio, args.output)
    except Exception as e:
        print(f"An error occurred: {e}")
