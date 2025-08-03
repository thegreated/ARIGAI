from content_generator.ArticleController import ArticleController
from content_generator.helper.GeminiTTS import GeminiTTS
from video_generator.VideoBuilder import VideoBuilder
from video_generator.VideoBuilder_old_backup import *
from dotenv import load_dotenv
#from video_generator.helper.GeminiTTS import  GeminiTTS
import  os

from video_generator.helper.TextToAudio import TextToAudio

link = "https://test-website.com"
load_dotenv()

# generate and get the article and images
output_data = ArticleController(link).generate_article()
# covert to audio

output_data['narrator']=  GeminiTTS().generate(output_data['article'])


#finalizing the data combining it together
sub = VideoBuilder.generate(
    output_data['images'],
    "resources/background_music.mp3",
    output_data['narrator'],
     os.getenv("OUTPUT_PATH")+"final_reels.mp4"
     )



