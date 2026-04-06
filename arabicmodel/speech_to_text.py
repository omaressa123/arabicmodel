import whisper
import os
from .config import WHISPER_SETTINGS

class ArabicSpeechToText:
    def __init__(self, model_size=WHISPER_SETTINGS['model_size']):  
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path):
        """Transcribe the audio file to text."""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found at: {audio_path}")
        
        result = self.model.transcribe(audio_path, language=WHISPER_SETTINGS['language'])
        return result['text']

# Example usage
if __name__ == '__main__':
    stt = ArabicSpeechToText()
    # Replace with a real audio file for testing
    # result = stt.transcribe('test_audio.wav')  
    # print(result)