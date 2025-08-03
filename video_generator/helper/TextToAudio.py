from gtts import gTTS
import  os
class TextToAudio:


    @staticmethod
    def generate(text):
        tts = gTTS(text=text, lang='en', slow=False)

        # Save the audio to a file
        file_path =  os.getenv("NARRATION_PATH")+"narration.wav"
        tts.save(os.getenv(file_path))
        return  file_path
