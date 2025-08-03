import os
import json
import whisper
from moviepy.editor import (
    AudioFileClip, CompositeVideoClip, CompositeAudioClip,
    TextClip, ImageClip, concatenate_videoclips
)
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.fx.all import audio_loop
from moviepy.config import change_settings

change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
})

class AudiogramFromAudio:
    def __init__(self, narration_path, bg_images, bg_music=None, font="Arial-Bold"):
        self.narration = narration_path
        self.bg_images = bg_images
        self.bg_music = bg_music
        self.font = font
        self.video_size = (1080, 1920)

        self.wordlevel_info = []
        self.subtitles = []


def transcribe(self):
    print("Transcribing with Whisper...")
    model = whisper.load_model("medium")
    result = model.transcribe(self.audio_path, word_timestamps=True)
    for segment in result["segments"]:
        for word in segment["words"]:
            self.wordlevel_info.append({
                'word': word['word'].strip(),
                'start': word['start'],
                'end': word['end']
            })
    with open("data.json", "w") as f:
        json.dump(self.wordlevel_info, f, indent=4)


def load_wordlevel_json(self, path='data.json'):
    with open(path, 'r') as f:
        self.wordlevel_info = json.load(f)


def split_to_lines(self, max_chars=80, max_duration=3.0, max_gap=1.5):
    print("Splitting into line-level subtitles...")
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
    full_duration = line_json['end'] - line_json['start']
    word_clips = []
    positions = []

    x, y = 0, 0
    w, h = self.frame_size
    x_buf = w // 10
    y_buf = h // 5

    for word_data in line_json['textcontents']:
        duration = word_data['end'] - word_data['start']
        word = word_data['word']

        word_clip = TextClip(word, font=self.font, fontsize=self.fontsize, color=self.fg_color)
        space_clip = TextClip(" ", font=self.font, fontsize=self.fontsize, color=self.fg_color)
        word_clip = word_clip.set_start(line_json['start']).set_duration(full_duration)
        space_clip = space_clip.set_start(line_json['start']).set_duration(full_duration)

        word_w, word_h = word_clip.size
        space_w, _ = space_clip.size

        if x + word_w + space_w > w - 2 * x_buf:
            x = 0
            y += word_h + 40

        pos = (x + x_buf, y + y_buf)
        word_clip = word_clip.set_position(pos)
        space_clip = space_clip.set_position((pos[0] + word_w, pos[1]))

        highlight = TextClip(word, font=self.font, fontsize=self.fontsize,
                             color=self.fg_color, bg_color=self.bg_color)
        highlight = highlight.set_start(word_data['start']).set_duration(duration).set_position(pos)

        word_clips.extend([word_clip, space_clip, highlight])
        x += word_w + space_w

    return word_clips


def generate_video(self, output_path="audiogram_output.mp4"):
    print("Rendering video...")
    all_clips = []
    for line in self.linelevel_subtitles:
        all_clips.extend(self.create_caption(line))

    background = ColorClip(size=self.frame_size, color=(0, 0, 0), duration=self.duration)
    final = CompositeVideoClip([background] + all_clips)
    final = final.set_audio(self.audio_clip)
    final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")


bg_imgs = [
    "C:/python_resources/generated_article_images/initial_image_data/test_1.webp",
    "C:/python_resources/generated_article_images/initial_image_data/test_2.webp",
    "C:/python_resources/generated_article_images/initial_image_data/test_3.jpg",
]

narration_audio = "C:/python_resources/narration/narration.wav"
bg_music_audio = "C:/Users/jaz2/Documents/PythonProject/resources/background_music.mp3"

audiogram = AudiogramFromAudio(
    narration_path=narration_audio,
    bg_images=bg_imgs,
    bg_music=bg_music_audio,
)

audiogram.generate("final_audiogram_final_2.mp4")