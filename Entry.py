from Comment import Comment, CommentTree
class Entry:
    def __init__(self, json_entry, comments: CommentTree = None):
        self.id = json_entry['id']
        self.title = json_entry['title']
        self.intro = json_entry['intro']
        self.comments = comments
        self.auth_id = json_entry["author"]["id"]
        self.auth_name = json_entry["author"]["name"]
        self.comments_count = len(self.comments) if comments is not None else 0
        self.my_comments = comments
    
    def get_entry_as_dict(self)->dict:
        result = {
                    "id": self.id,
                    "title": self.title,
                    "intro": self.intro ,
                    "comments": self.comments.get_all_comments_as_dict(),
                    "comments_count":self.comments_count
                }
        return result
    
    def set_comments(self, new_comments: CommentTree)->None:
        self.comments = new_comments
        self.comments_count = len(self.comments.all_comments)

    def __str__(self)->str:
        return self.intro + '\n' + self.title
    
    def __sub__(self, other)->CommentTree: # - вычитание (x - y)
        """Возвращает CommentTree новых комментариев"""
        set_self = set(self.comments.get_all_comments_as_dict())
        set_other = set(other.comments.get_all_comments_as_dict())
        difference = set_other - set_self
        return CommentTree(list(difference), self.id)
    
    def set_updates(self, new)->CommentTree:
        """Устанавливает обновленные комментарии в записи. Возвращает новые комментарии, очищенные от комментариев автора.
            new - обвновленная версия записи."""
        if self.id == new.id:
            self.set_comments(new.comments)
            return self.__sub__(new).get_comments_without_author(self.auth_name)
    
