
class ArticleModel:

    def __init__(self,title,body,image_location):
        self.title = title
        self.body = body
        self.image_location = image_location

    def get_title(self):
        return self.title

    def get_body(self):
        return  self.body


