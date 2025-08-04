from content_generator.helper.ImageConfig import ImageConfig
from content_generator.helper.OpenAIConfig import OpenAIConfig
from dotenv import load_dotenv
import os

class OpenAI:

    def __init__(self):
        self.prompt = ("Revised the article "
                       "make it interesting ,"
                       "make it 1 minute long,"
                       "create an interesting title for the article,"
                       "The article should be direct to the point approach,"
                       "the output should be only json format like this with title and article, "
                       "i need it to be json only  i want to use the data "
                       "this is the article: ")

        self.prompt_character= ("Based on this article list all the characters accordingly "
                               "Make sure to sort it by the when the article mention on the character"
                               " for example if character 1 mention first it should be 1st on array "
                               "The only data on the array should be the name of the character only "
                                "Among this character or topic pic 3 that most relevant to the article"
                                "Don't mension any company or the original creator of the article"
                                "No other data just the name of the character" 
                                "The character is only human or animals"
                               "this is the article: ")



    def revised_article(self, article_body):
        print("Revising the article.")
        # revised article
        openai_revised_body =  OpenAIConfig.generateContent(self.prompt,article_body)
        print(openai_revised_body)
        return  openai_revised_body

    def list_of_images_character(self,article_body):
        print("Sorting the images by article story.")
        openai_character = OpenAIConfig.generateContent(self.prompt_character, article_body)
        print(openai_character)
        return openai_character












