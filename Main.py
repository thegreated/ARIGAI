from content_generator.ArticleController import ArticleController
from video_generator.VideoBuilder import *
from dotenv import load_dotenv
#from video_generator.helper.GeminiTTS import  GeminiTTS
import  os

from video_generator.helper.TextToAudio import TextToAudio

link = "https://test-website.com"
load_dotenv()

# generate and get the article
output_data = ArticleController(link).generate_article()
# covert to audio
output_data['narrator']= TextToAudio().generate(output_data['article'])


#finalizing the data combining it together
sub = SubTitleController(
    output_data['narrator'],
    output_data['images'],
   "resources/background_music.mp3",
        os.getenv("OUTPUT_PATH")+"final_reels.mp4"
           )

sub.process_raw_audio()



