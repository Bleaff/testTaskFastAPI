from Comment import *
class Entry:
    def __init__(self, json_entry, comments: CommentTree):
        self.id = json_entry['id']
        self.title = json_entry['title']
        self.intro = json_entry['intro']
        self.all_comments = comments
        self.auth_id = json_entry["author"]["id"]
        self.auth_name = json_entry["author"]["name"]
        self.comments_count = len(self.all_comments)
        self.my_comments = comments
    
    def get_entry_as_dict()->dict:
        result = {
                    "id": self.id,
                    "title": self.title,
                    "intro": self.intro,
                    "comments": self.all_comments.get_all_comments_as_dict()
                }
    
    def __str__(self)->str:
        return self.intro + '\n' + self.title
    
    def __sub__(self, other)->CommentTree: # - вычитание (x - y)
        """Возвращает CommentTree новых комментариев"""
        set_self = set(self.all_comments.get_all_comments())
        set_other = set(other.all_comments.get_all_comments())
        difference = set_other - set_self
        new = Entry()
        return CommentTree(list(difference), self.id)
    
    def set_updates(self, new:Entry)->CommentTree:
        """Устанавливает обновленные комментарии в записи. Возвращает комментарии, очищенные от комментариев автора."""
        if self.id == new.id:
            self.all_comments = new.all_comments.get_all_comments()
            self.comments_count = new.comments_count
            self.all_comments = new.all_comments.get_all_comments()
            res = self.__sub__(new).get_comments_without_author(self.auth_name)
            return 

