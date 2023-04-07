from Comment import Comment, CommentTree
class Entry:
    def __init__(self, json_entry, comments: CommentTree = None, marked:CommentTree = None):
        self.id = json_entry['id']
        self.title = json_entry['title']
        self.intro = ''
        self.comments = comments
        self.auth_id = json_entry["author"]["id"]
        self.auth_name = json_entry["author"]["name"]
        self.comments_count = len(self.comments) if comments is not None else 0
        self.marked_comments = marked
        for block in json_entry['blocks']:
            if block['type'] == 'text' or block['type'] == 'incut' or block['type'] == 'header':
                self.intro += block['data']['text'] + '\n'
            elif block['type'] == 'list':
                for item in block['data']['items']:
                    self.intro += item + '\n'
    
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
        return self.intro + ' ' + self.title

    def get_differ_comments(self, other):
        """Возвращает CommentTree только c новыми комментариями."""
        self_set_comments = set([comment['id'] for comment in self.comments.get_all_comments_as_dict()]) # Получаем множество комментариев в виде списка id комментариев, используем свойство их уникальности
        other_set_comments = set([comment['id'] for comment in other.comments.get_all_comments_as_dict()])
        difference = list(self_set_comments - other_set_comments) # Множество разности приводится к списку и затем подключаем комментарии по этим id
        return self.comments.get_comments_by_id(difference)

    def set_updates(self, new):
        """Устанавливает обновленные комментарии в записи. Возвращает новые комментарии, очищенные от комментариев автора.
            new - обвновленная версия записи."""
        if self.id == new.id:
            difference = new.get_differ_comments(self)
            self.set_comments(new.comments)
            return difference.get_comments_without_author(self.auth_name)
    
