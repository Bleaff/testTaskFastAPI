class Comment:
    def __init__(self, id, auth_name, media, reply_to, text, lvl):
        self._id = id
        self._author_name = auth_name
        self._media = media
        self._reply_to = reply_to
        self._text = text
        self._level = lvl
        self.time = 0
        self.answers = []
    def __str__(self):
        """Trail version of this method"""
        return f"{self._author_name}: {self._text} <|endofstatement|>"
    
    def get_answers(self):
        return answers.copy()
