
import whisper

class AudioProcessor:
    def __init__(self, audio_path, model_size="base"):
        self.audio_path = audio_path
        self.model = whisper.load_model(model_size)

    def transcribe(self):
        print("Transcribing audio...")
        result = self.model.transcribe(self.audio_path)
        return result.get("segments", [])