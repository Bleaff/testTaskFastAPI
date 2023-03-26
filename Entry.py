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

    @staticmethod
    def copy_entry(entry:Entry)->Entry:
        json_entry = {'id':entry.id, 
                        'title':entry.title, 
                        'intro':entry.intro,
                        'author':{
                            'id':entry.auth_id,
                            'name':entry.auth_name}
        }
        return Entry(json_entry, entry.comments)
    
    def __sub__(self, other): # - вычитание (x - y)
        """Возвращает Entry c только новыми комментариями."""
        self_set_comments = set([comment['id'] for comment in self.comments.get_all_comments_as_dict()]) # Получаем множество комментариев в виде списка id комментариев, используем свойство их уникальности
        other_set_comments = set([comment['id'] for comment in other.comments.get_all_comments_as_dict()]) 
        difference = list(set_other - set_self) # Множество разности приводится к списку и затем подключаем комментарии по этим id
        diff_entry = Entry.copy_entry(other)
        diff_entry.set_comments(other.comments.get_comments_by_id(difference)) 
        return diff_entry
    
    def set_updates(self, new)->CommentTree:
        """Устанавливает обновленные комментарии в записи. Возвращает новые комментарии, очищенные от комментариев автора.
            new - обвновленная версия записи."""
        if self.id == new.id:
            self.set_comments(new.comments)
            return self.__sub__(new).comments.get_comments_without_author(self.auth_name)
    
