from moviepy.editor import ColorClip, CompositeVideoClip, TextClip
import os
import platform
import subprocess
from moviepy.config import change_settings

from video_generator.helper.SubtitleText import SubtitleText


class Test:
    font_path = "C:/Users/jaz2/Documents/PythonProject/resources/fonts/RobotoSlab-ExtraBold.ttf"
    change_settings({
        "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
    })


    @staticmethod
    def make_generator(video_clip, *,
                       font=font_path,
                       fontsize=72,
                       stroke_width=3,
                       margin_px=40,
                       safe_fraction=0.9):
        maxw = int(video_clip.w * safe_fraction) - 2 * margin_px
        return lambda txt: (
            TextClip(txt,
                     font=font,
                     fontsize=fontsize,
                     color='white',
                     stroke_color='black',
                     stroke_width=stroke_width,
                     method='caption',
                     size=(maxw, None),
                     align='center',
                     interline=4)
            .set_position(('center', 'bottom'))
        )

    def open_file(filepath):
        if platform.system() == 'Windows':
            os.startfile(filepath)
        elif platform.system() == 'Darwin':
            subprocess.run(['open', filepath])
        else:
            subprocess.run(['xdg-open', filepath])

    if __name__ == "__main__":
        # Reels size: 1080x1920 (vertical)
        reels_size = (1080, 1920)
        video = ColorClip(size=reels_size, color=(0, 0, 255), duration=5)

        # Generate subtitle
        make_clip = make_generator(video)
        sample_text = "This is a long subtitle to test if it wraps properly and fits the Reels format without going out of frame."
        subtitle_clip = make_clip(sample_text).set_duration(5)

        # Combine and export
        output_path = "test_subtitle_reels.mp4"
        final = CompositeVideoClip([video, subtitle_clip])
        final.write_videofile(output_path, fps=24)

        # Auto open
        open_file(output_path)