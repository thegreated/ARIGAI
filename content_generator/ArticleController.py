
from content_generator.OpenAI import OpenAI
from content_generator.WebScrapping import WebScrapping


class ArticleController:

    def __init__(self,article_link):
        self.article_link = article_link


    def generate_article(self):

        article_body= WebScrapping.generate_articleScrapping(self.article_link)
        openai = OpenAI()
        article_revised = openai.revised_article(article_body)

        return  article_revised















