import nltk

class Chatty():
    def __init__(self):
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_words = ['?', '!']