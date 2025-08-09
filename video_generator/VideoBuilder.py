
import json
import whisper
from moviepy.editor import (
    TextClip, CompositeVideoClip, ColorClip, AudioFileClip
)
from moviepy.config import change_settings
from moviepy.editor import ImageClip, concatenate_videoclips
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.fx.all import audio_loop

from moviepy.editor import (
    AudioFileClip, CompositeVideoClip, TextClip,
    CompositeAudioClip
)
import os

from faster_whisper import WhisperModel


class VideoBuilder:
    change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

    def __init__(self, audio_path, bg_images, bg_music, output_name, frame_size=(1080, 1920),
                 font="Helvetica-Bold", fontsize=70,
                 fg_color='white', bg_color='blue'):
        self.audio_path = audio_path
        self.bg_images = bg_images
        self.bg_music = bg_music
        self.output_name = output_name
        self.wordlevel_info = []
        self.linelevel_subtitles = []
        self.frame_size = frame_size
        self.font = font
        self.fontsize = fontsize
        self.fg_color = fg_color
        self.bg_color = bg_color

        self.audio_clip = AudioFileClip(audio_path)
        self.duration = self.audio_clip.duration
    def transcribe(self):
        print("Transcribing with Faster-Whisper...")

        # Choose a small model for speed (e.g., "base", "tiny")
        model = WhisperModel("base", compute_type="int8", device="cpu")  # use "cuda" if GPU available

        segments, _ = model.transcribe(self.audio_path, word_timestamps=True)

        self.wordlevel_info = []
        for segment in segments:
            for word in segment.words:
                self.wordlevel_info.append({
                    'word': word.word.strip(),
                    'start': word.start,
                    'end': word.end
                })

        # Save to JSON
        json_path = os.path.join(os.getenv("JSON_FILES", "./"), "narration.json")
        with open(json_path, "w") as f:
            json.dump(self.wordlevel_info, f, indent=4)

    def split_to_lines(self, max_chars=80, max_duration=3.0, max_gap=1.5):
        print("------ Splitting into line-level subtitles...")
        data = self.wordlevel_info
        subtitles = []
        line = []
        line_duration = 0

        for i, word in enumerate(data):
            line.append(word)
            line_duration += word["end"] - word["start"]
            temp = " ".join(w["word"] for w in line)

            chars_exceeded = len(temp) > max_chars
            duration_exceeded = line_duration > max_duration
            gap_exceeded = i > 0 and (word["start"] - data[i - 1]["end"] > max_gap)

            if chars_exceeded or duration_exceeded or gap_exceeded:
                subtitles.append({
                    "word": " ".join(w["word"] for w in line),
                    "start": line[0]["start"],
                    "end": line[-1]["end"],
                    "textcontents": line
                })
                line = []
                line_duration = 0

        if line:
            subtitles.append({
                "word": " ".join(w["word"] for w in line),
                "start": line[0]["start"],
                "end": line[-1]["end"],
                "textcontents": line
            })

        self.linelevel_subtitles = subtitles

    def create_caption(self, line_json):
        print("------ Creating Centered Captions...")
        full_duration = line_json['end'] - line_json['start']
        w, h = self.frame_size

        x_buf = w // 10
        max_width = w - 2 * x_buf
        line_spacing = 40

        current_line = []
        lines = []
        line_width = 0
        word_height = 0

        for word_data in line_json['textcontents']:
            word = word_data['word']
            word_clip = TextClip(word, font=self.font, fontsize=self.fontsize, color=self.fg_color).set_duration(full_duration)
            space_clip = TextClip(" ", font=self.font, fontsize=self.fontsize, color=self.fg_color).set_duration(full_duration)

            word_w, word_h = word_clip.size
            space_w, _ = space_clip.size
            total_w = word_w + space_w

            if line_width + total_w > max_width and current_line:
                lines.append((current_line, line_width))
                current_line = []
                line_width = 0

            current_line.append((word_clip, space_clip, word_data))
            line_width += total_w
            word_height = word_h

        if current_line:
            lines.append((current_line, line_width))

        total_height = len(lines) * (word_height + line_spacing) - line_spacing
        y_offset = -500
        y_start = (h - total_height - y_offset) // 2

        word_clips = []
        for i, (line, line_width) in enumerate(lines):
            x_start = (w - line_width) // 2
            y = y_start + i * (word_height + line_spacing)
            x = x_start

            padding = 20
            bg_width = line_width + padding
            bg_height = word_height + padding

            line_bg = ColorClip(size=(bg_width, bg_height), color=(0, 0, 0)).set_opacity(0.8).set_duration(full_duration)
            line_bg = line_bg.set_position((x_start - padding // 2, y - padding // 2)).set_start(line_json['start'])
            word_clips.append(line_bg)

            for word_clip, space_clip, word_data in line:
                word_w, _ = word_clip.size
                space_w, _ = space_clip.size
                pos = (x, y)

                word_clip = word_clip.set_start(line_json['start']).set_position(pos)
                space_clip = space_clip.set_start(line_json['start']).set_position((x + word_w, y))

                highlight = TextClip(
                    word_data['word'],
                    font=self.font,
                    fontsize=self.fontsize,
                    color=self.fg_color,
                    bg_color=self.bg_color
                ).set_start(word_data['start']).set_duration(word_data['end'] - word_data['start']).set_position(pos)

                word_clips.extend([word_clip, space_clip, highlight])
                x += word_w + space_w

        return word_clips

    def generate_video(self,title_text):
        print(" ------Rendering video...")

        all_clips = []


        title_fontsize = self.fontsize - 30
        w, h = self.frame_size

        title_clip = TextClip(title_text, fontsize=title_fontsize, font=self.font, color='black', method='caption', size=(w - 66, None)).set_duration(self.duration)
        title_w, title_h = title_clip.size
        inner_padding_top = 170
        inner_padding_side = 100
        inner_padding_bottom = 30
        bg_width = title_w + inner_padding_side
        bg_height = title_h + inner_padding_top + inner_padding_bottom

        title_bg = ColorClip(size=(bg_width, bg_height), color=(255, 255, 255)).set_duration(self.duration)
        title_bg = title_bg.set_position(('center', 0))

        title_clip = title_clip.set_position(('center', inner_padding_top))

        all_clips.append(title_bg)
        all_clips.append(title_clip)
        # ------------------

        for line in self.linelevel_subtitles:
            all_clips.extend(self.create_caption(line))

        return all_clips

    def generate_bg(self, title):
        print("Combining all together...")
        speech = AudioFileClip(self.audio_path)
        speech_duration = speech.duration
        image_duration = speech_duration / len(self.bg_images)

        # Define padding (e.g., 50px on all sides)
        inner_padding = 280
        video_width = 1080
        video_height = 1920
        padded_width = video_width - 2 * inner_padding
        padded_height = video_height - 2 * inner_padding

        bg_clips = [
            ImageClip(img)
            .resize(height=padded_height)  # Resize to fit inside padding
            .on_color(
                size=(video_width, video_height),
                color=(0, 0, 0),  # Black background
                pos='center'  # Center the image
            )
            .set_duration(image_duration)
            for img in self.bg_images
        ]

        bg_clip = concatenate_videoclips(bg_clips, method="compose")

        # Add and loop background music
        bg_music = volumex(AudioFileClip(self.bg_music), 0.03)
        bg_music = audio_loop(bg_music, duration=speech_duration)
        final_audio = CompositeAudioClip([speech, bg_music])

        # Apply audio to video
        video_with_audio = bg_clip.set_audio(final_audio)

        # Add subtitles/title overlays
        subtitles = self.generate_video(title)
        final_clip = CompositeVideoClip([video_with_audio] + subtitles)

        # Export the final video
        final_clip.write_videofile(
            self.output_name,
            fps=24,
            codec="libx264",  # CPU encoding
            audio_codec="aac",
            preset="fast",  # Or "slow" for better compression
            bitrate="5M"
        )
        speech.close()

    @staticmethod
    def generate(title,bg_images, bg_music_audio, narration_path, output_names):
        generator = VideoBuilder(audio_path=narration_path, bg_images=bg_images, bg_music=bg_music_audio, output_name=output_names)
        generator.transcribe()
        generator.split_to_lines()
        generator.generate_bg(title)

