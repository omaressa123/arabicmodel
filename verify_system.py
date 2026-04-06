import json
import requests
from arabicmodel.text_cleaning import preprocess_text
from arabicmodel.slide_generator import SlideGenerator
from arabicmodel.config import OLLAMA_API_URL, OLLAMA_SETTINGS, OUTPUT_DIR
import os

def test_llm_and_slides(topic_text):
    """Test the LLM and Slide Generator components."""
    print(f"--- Testing with Topic: {topic_text} ---")
    
    # 1. Clean Text
    cleaned_text = preprocess_text(topic_text)
    print(f"Cleaned Text: {cleaned_text}")
    
    # 2. LLM Generation
    prompt = f"""
    Generate a structured presentation in JSON format for the following topic: "{cleaned_text}".
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
    
    print("Requesting from Ollama...")
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        llm_response = response.json().get('response', '').strip()
        
        # Extract JSON
        start = llm_response.find('[')
        end = llm_response.rfind(']') + 1
        if start != -1 and end != -1:
            json_str = llm_response[start:end]
            slides_data = json.loads(json_str)
            print("Successfully parsed JSON from LLM.")
        else:
            print(f"Failed to find JSON in response: {llm_response}")
            return
            
    except Exception as e:
        print(f"Error: {e}")
        return

    # 3. Slide Generation
    print("Generating PowerPoint...")
    generator = SlideGenerator()
    output_path = generator.create_presentation(slides_data, "test_verification.pptx")
    
    if output_path and os.path.exists(output_path):
        print(f"Success! Verification presentation saved at: {output_path}")
    else:
        print("Failed to save presentation.")

if __name__ == "__main__":
    # Test with a typical Egyptian Arabic request
    test_topic = "اعمل برزنتيشن عن مستقبل الذكاء الاصطناعي في مصر وكده"
    test_llm_and_slides(test_topic)
