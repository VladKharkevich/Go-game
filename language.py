import json


class Language:

    def __init__(self):
        self.current_language = 'english'
        self.change_language(self.current_language)

    def change_language(self, language):
        self.current_language = language
        with open('languages/' + language + '.json', 'r') as f:
            self.data = json.load(f)


lang = Language()
