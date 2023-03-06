class CommentTree:
    def __init__(self, comments_list :list, entry_id :int) -> None:
        self._comments_list = comments_list
        self._entry_id = entry_id
    
    def make_full_tree():
        ...
        

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
    def __str__(self) -> str:
        """Trail version of this method"""
        return f"{self._author_name}: {self._text} <|endofstatement|>"
    
    def get_answers(self) -> list:
        return self.answers.copy()
    
    # def to_send(self):
    #     return {"text": f"{self._text}", "reply_to": f"{self._reply_to}","attachments": "[]"}
