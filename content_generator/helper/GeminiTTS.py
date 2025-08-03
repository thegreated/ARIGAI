
from google import genai
from google.genai import types
import wave
import os

class GeminiTTS:


    def generate(self,article):
        print("Converting article to  audio ....")
        client = genai.Client(api_key="AIzaSyBplOt4yUrjLQKSnTQ2WbnzVB0eXf_G_EI")
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents= article,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name='Kore',
                        )
                    )
                ),
            )
        )

        data = response.candidates[0].content.parts[0].inline_data.data

        exact_path = os.getenv("NARRATION_PATH")+"narration.wav"
        print(exact_path)
        self.wave_file(exact_path, data)  # Saves the file to current directory
        return exact_path

    # Set up the wave file to save the output:
    @staticmethod
    def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
       with wave.open(filename, "wb") as wf:
          wf.setnchannels(channels)
          wf.setsampwidth(sample_width)
          wf.setframerate(rate)
          wf.writeframes(pcm)




