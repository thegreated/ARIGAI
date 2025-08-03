from moviepy.editor import CompositeVideoClip, ColorClip
import random
import os
from video_generator.helper.TestTranscript import *

from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

# Create a dummy line_json to simulate real subtitle data
fake_line_json = {
    "start": 0.5,
    "end": 5.5,
    "textcontents": [
        {"word": "This are the", "start": 0.5, "end": 1.0},
        {"word": "random", "start": 1.1, "end": 1.4},
        {"word": "a", "start": 1.5, "end": 1.6},
        {"word": "test", "start": 1.7, "end": 2.2},
        {"word": "caption", "start": 2.3, "end": 3.0}
    ]
}


# Dummy class instance to access method

generator = TestTranscript(
    audio_path="C:/python_resources/narration/narration.wav",  # not used in this test
    bg_images=["C:/python_resources/generated_article_images/initial_image_data/test_1.webp"],
    bg_music="C:/Users/jaz2/Documents/PythonProject/resources/background_music.mp3",
    output_name="test_caption_output.mp4",
    frame_size=(1080, 1920)
)

# Generate the caption layer
caption_clips = generator.create_caption(fake_line_json)

# Create a solid color background (for visual contrast)
bg = ColorClip(size=generator.frame_size, color=(20, 20, 20), duration=5.5)

# Combine background + subtitles
final_clip = CompositeVideoClip([bg] + caption_clips)

# Export to video
final_clip.write_videofile("test_caption_output.mp4", fps=24)




