from moviepy.editor import TextClip, ColorClip, CompositeVideoClip
import os
from moviepy.config import change_settings

class CaptionTester:
    change_settings({
        "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
    })

    def __init__(self):
        self.frame_size = (1080, 1920)
        self.font = "Arial"  # Make sure this font is installed or adjust as needed
        self.fontsize = 50
        self.fg_color = "white"
        self.bg_color = "red"  # Highlight color

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

        # First pass: group words into lines
        for word_data in line_json['textcontents']:
            word = word_data['word']

            word_clip = TextClip(
                word,
                font=self.font,
                fontsize=self.fontsize,
                color=self.fg_color,
            ).set_duration(full_duration)

            space_clip = TextClip(
                " ",
                font=self.font,
                fontsize=self.fontsize,
                color=self.fg_color
            ).set_duration(full_duration)

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
        y_offset = -500  # Adjust as needed
        y_start = (h - total_height - y_offset) // 2

        word_clips = []
        for i, (line, line_width) in enumerate(lines):
            x_start = (w - line_width) // 2
            y = y_start + i * (word_height + line_spacing)
            x = x_start

            padding = 20
            bg_width = line_width + padding
            bg_height = word_height + padding

            line_bg = ColorClip(
                size=(bg_width, bg_height),
                color=(0, 0, 0)
            ).set_opacity(0.8).set_duration(full_duration)

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
                    bg_color=self.bg_color,
                ).set_start(word_data['start']).set_duration(
                    word_data['end'] - word_data['start']
                ).set_position(pos)

                word_clips.extend([word_clip, space_clip, highlight])
                x += word_w + space_w

        return word_clips


test_line_json = {
    "start": 0.0,
    "end": 5.0,
    "textcontents": [
        {"word": "Hello world", "start": 0.0, "end": 1.0},
        {"word": "This is greatest,", "start": 1.0, "end": 2.0},
        {"word": "and lmao", "start": 2.0, "end": 3.0},
        {"word": "on the", "start": 3.0, "end": 4.0},
        {"word": "world!", "start": 4.0, "end": 5.0}
    ]
}

tester = CaptionTester()
clips = tester.create_caption(test_line_json)

background = ColorClip(tester.frame_size, color=(30, 30, 30)).set_duration(5)
video = CompositeVideoClip([background] + clips)
video.write_videofile("test_caption.mp4", fps=24)
os.startfile("test_caption.mp4")