import whisper
import os
import subprocess
from .config import WHISPER_SETTINGS

class ArabicSpeechToText:
    def __init__(self, model_size=WHISPER_SETTINGS['model_size']):  
        self._check_ffmpeg()
        self.model = whisper.load_model(model_size, device=WHISPER_SETTINGS['device'])

    def _check_ffmpeg(self):
        """Check if ffmpeg is installed and available in the PATH."""
        try:
            subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: ffmpeg not found. Whisper might fail for some audio formats.")
            # We don't raise an error yet, because some users might have it in a custom path or only use formats that don't need it.

    def transcribe(self, audio_path):
        """Transcribe the audio file to text."""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found at: {audio_path}")
        
        try:
            result = self.model.transcribe(
                audio_path, 
                language=WHISPER_SETTINGS['language'], 
                task=WHISPER_SETTINGS['task'],
                fp16=WHISPER_SETTINGS['fp16'],
                verbose=False
            )
            return result['text']
        except Exception as e:
            if "ffmpeg" in str(e).lower() or "[WinError 2]" in str(e):
                raise RuntimeError("خطأ: برنامج ffmpeg غير مثبت على النظام. يرجى تثبيته لتتمكن من معالجة ملفات الصوت.") from e
            raise e

# Example usage
if __name__ == '__main__':
    stt = ArabicSpeechToText()
    # Replace with a real audio file for testing
    # result = stt.transcribe('test_audio.wav')  
    # print(result)