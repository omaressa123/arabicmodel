import os
import requests

# Define the URL for the Whisper model
model_url = 'https://example.com/path/to/whisper/model'

# Function to download the model
def download_model(model_url, save_path):
    response = requests.get(model_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as model_file:
            model_file.write(response.content)
        print(f'Model downloaded and saved to {save_path}')
    else:
        print('Failed to download model. Status code:', response.status_code)

if __name__ == '__main__':
    save_path = 'whisper_model.bin'  # Change the path as needed
    download_model(model_url, save_path)

# Ollama Setup Instructions:
# 1. Install Ollama by running: `pip install ollama`
# 2. Load the model in Ollama using: `ollama load whisper_model.bin`
# 3. Once loaded, you can use the model for inference.
