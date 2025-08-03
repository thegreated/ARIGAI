import os
import json
import whisper
from moviepy.editor import (
    TextClip, CompositeVideoClip, ColorClip, AudioFileClip
)


class AudiogramFromAudio:
    def __init__(self, audio_path, frame_size=(1080, 1080),
                 font="Helvetica-Bold", fontsize=80,
                 fg_color='white', bg_color='blue'):
        self.audio_path = audio_path
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


generator = AudiogramFromAudio(audio_path="your_audio.mp3")

generator.transcribe()
generator.split_to_lines()
generator.generate_video("final_output.mp4")