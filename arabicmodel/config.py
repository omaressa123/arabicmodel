# config.py
import os
import torch

# Project Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model Paths (optional, using default locations for Whisper and Ollama)
WHISPER_MODEL_NAME = 'base' # 'base', 'small', 'medium', 'large'

# Whisper Model Settings
WHISPER_SETTINGS = {
    'language': 'ar',
    'model_size': WHISPER_MODEL_NAME,
    'task': 'transcribe',
    'fp16': torch.cuda.is_available(),  # Use FP16 only if CUDA is available
    'device': 'cuda' if torch.cuda.is_available() else 'cpu'
}

# Ollama Settings
OLLAMA_MODEL_NAME = 'mistral'
OLLAMA_API_URL = 'http://localhost:11434/api/generate'

OLLAMA_SETTINGS = {
    'model': OLLAMA_MODEL_NAME,
    'options': {
        'num_predict': 1024,
        'temperature': 0.7,
    }
}

# Project Structure
DATA_DIR = os.path.join(BASE_DIR, 'audio')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

for directory in [DATA_DIR, OUTPUT_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)