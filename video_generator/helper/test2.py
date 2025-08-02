from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from moviepy.config import change_settings

import os
import sys
import subprocess


change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
})


def open_file(path):
    """Open file with default system viewer."""
    if sys.platform.startswith("darwin"):
        subprocess.call(("open", path))
    elif os.name == "nt":
        os.startfile(path)
    elif os.name == "posix":
        subprocess.call(("xdg-open", path))

def generate_video_with_shadow():
    txt = "This is a long subtitle to test if it wraps properly and fits the Reels format without going out of frame."
    fontsize = 72
    font = "Arial-Black"
    duration = 5
    video_size = (1080, 1920)

    # Background
    bg = ColorClip(video_size, color=(30, 30, 30), duration=duration)

    # Shadow (slightly offset)
    shadow = TextClip(
        txt,
        fontsize=fontsize,
        font=font,
        color='black',
        method='caption',
        size=(1000, None),
        align='center'
    ).set_position(('center', 704)).set_duration(duration)

    # Main text
    text = TextClip(
        txt,
        fontsize=fontsize,
        font=font,
        color='white',
        stroke_color='black',
        stroke_width=3,
        method='caption',
        size=(1000, None),
        align='center'
    ).set_position(('center', 700)).set_duration(duration)

    final = CompositeVideoClip([bg, shadow, text])
    output_path = "shadowed_subtitle.mp4"
    final.write_videofile(output_path, fps=24)

    # Auto-open after render
    open_file(output_path)

generate_video_with_shadow()