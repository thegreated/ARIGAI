
from content_generator.OpenAI import OpenAI
from content_generator.WebScrapping import WebScrapping
from google_image_search.ImageSearch import ImageSearch

class ArticleController:

    def __init__(self,article_link):
        self.article_link = article_link


    def generate_article(self):

        article_body= WebScrapping.generate_articleScrapping(self.article_link)
        openai = OpenAI()
        article_revised = openai.revised_article(article_body)
        list_of_search_char = openai.list_of_images_character(article_body)
        article_revised['images'] = ImageSearch().search(list_of_search_char)

        return  article_revised















