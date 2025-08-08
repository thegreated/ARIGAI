from auto_upload.YoutubeUpload import YoutubeUpload
from content_generator.ArticleController import ArticleController
from content_generator.helper.GeminiTTS import GeminiTTS
from video_generator.VideoBuilder import VideoBuilder
from dotenv import load_dotenv
#from video_generator.helper.GeminiTTS import  GeminiTTS
import  os
import sys
from video_generator.helper.FileHandler import FileHandler
from video_generator.helper.GoogleSheet import GoogleSheet
import time

load_dotenv()

while True :

    infinite_handler = GoogleSheet().generate()
    print(infinite_handler)
    if infinite_handler :

        FileHandler.reset()
        link =  infinite_handler

        # generate and get the article and images

        output_data = ArticleController(link).generate_article()
        # covert to audio

        output_data['narrator']=  GeminiTTS().generate(output_data['article'])


        # get random background music
        random_bg_music = FileHandler.background_randomizer()


        final_video_full_path =  os.getenv("OUTPUT_PATH")+"final_reels.mp4"

        #finalizing the data combining it together
        sub = VideoBuilder.generate(
            output_data['title'],
            output_data['images'],
            random_bg_music,
            output_data['narrator'],
             final_video_full_path
             )


        YoutubeUpload().generate_upload(article_body = output_data['article'],
                                        article_title = output_data['title'],
                                        generated_video = final_video_full_path)

        GoogleSheet().change_status(output_data['title'])
    else:
        print("----------wait 1minute ")
        time.sleep(60)




