from content_generator.ArticleController import ArticleController
from content_generator.helper.GeminiTTS import GeminiTTS
from video_generator.VideoBuilder import VideoBuilder
from video_generator.helper.FileHandler import FileHandler
from dotenv import load_dotenv
load_dotenv()
FileHandler.reset()

link = "https://www.msn.com/en-ph/news/other/erwin-tulfo-10-or-more-congressmen-are-contractors-for-gov-t-projects/ar-AA1JZyBR?ocid=msedgdhp&pc=U531&cvid=8602db34acee4763b457d644504966dd&ei=43"


# generate and get the article and images

output_data = ArticleController(link).generate_article()
# covert to audio

output_data['narrator']=  GeminiTTS().generate(output_data['article'])

# get random background music
random_bg_music = FileHandler.background_randomizer()

#finalizing the data combining it together
sub = VideoBuilder.generate(
     output_data['title'],
     output_data['images'],
     random_bg_music,
     output_data['narrator']
     )

#FileHandler.reset()



