import re
import whisper

from video_generator.helper.AudioProcessor import AudioProcessor
from video_generator.helper.SubtitleGenerator import SubtitleGenerator
from moviepy.editor import (
    AudioFileClip, CompositeVideoClip, TextClip,
    CompositeAudioClip
)
from moviepy.audio.fx.volumex import volumex
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.audio.fx.all import audio_loop
from moviepy.config import change_settings
from moviepy.editor import ImageClip, concatenate_videoclips

from video_generator.helper.SubtitleText import SubtitleText


class SubTitleController:

    def __init__(self,narration,bg_images,bg_music,output_name):
        self.narration = narration
        self.bg_images = bg_images
        self.bg_music = bg_music
        self.output_name = output_name

        change_settings({
            "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
        })


    def process_raw_audio(self):

        speech = AudioFileClip(self.narration)
        speech_duration = speech.duration
        image_duration = speech_duration / len(self.bg_images)

        # Resize and pad/crop the image to 1080x1920 (vertical)
        bg_clips = [
            ImageClip(img)
            .resize(height=1920)
            .on_color(size=(1080, 1920), color=(0, 0, 0), pos=('center', 'center'))
            .set_duration(image_duration)
            for img in self.bg_images
        ]
        bg_clip = concatenate_videoclips(bg_clips, method="compose")

        # Load and loop background music
        bg_music = volumex(AudioFileClip(self.bg_music), 0.1)
        bg_music = audio_loop(bg_music, duration=speech_duration)
        final_audio = CompositeAudioClip([speech, bg_music])

        # Attach mixed audio to video
        video_with_audio = bg_clip.set_audio(final_audio)

        # Transcribe narration.mp3
        transcriber = AudioProcessor(self.narration)
        segments = transcriber.transcribe()

        # Generate subtitles from segments
        subtitle_gen = SubtitleGenerator(segments)
        subtitles_data = subtitle_gen.generate()

        # TextClip style generator
        generator = SubtitleText().make_generator(video_with_audio)
        # Build subtitles clip
        subtitles = SubtitlesClip(subtitles_data, make_textclip=generator).set_position(('center', 1300))

        # Combine Everything and Export ===

        final_clip = CompositeVideoClip([video_with_audio, subtitles])

        final_clip.write_videofile(self.output_name, fps=24, codec="libx264", audio_codec="aac")


