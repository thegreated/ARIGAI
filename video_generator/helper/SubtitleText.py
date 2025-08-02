from moviepy.video.VideoClip import TextClip


class SubtitleText:
    font_path = "C:/Users/jaz2/Documents/PythonProject/resources/fonts/RobotoSlab-ExtraBold.ttf"
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