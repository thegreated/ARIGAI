from content_generator.helper.ImageConfig import ImageConfig
from content_generator.helper.OpenAIConfig import OpenAIConfig
from dotenv import load_dotenv
import os

class OpenAI:

    def __init__(self):
        self.prompt = ("Revised the article "
                       "make it interesting ,"
                       "make it 5 seconds long,"
                       "create an interesting title for the article,"
                       "the output should be only json format like this with title and article, "
                       "i need it to be json only  i want to use the data "
                       "this is the article: ")



    def revised_article(self, article_body):
        print("Revising the article.")
        # revised article
        openai_revised_body =  OpenAIConfig.generateContent(self.prompt,article_body)
        # get the images
        img_config = ImageConfig(os.getenv("IMG_PATH"))
        openai_revised_body["images"] =  img_config.check_images_exist()
        return  openai_revised_body








