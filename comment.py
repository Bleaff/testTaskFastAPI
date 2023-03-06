from signalization import _error

class CommentTree:
	def __init__(self, comments_list :list, entry_id :int) -> None:
		self.all_comments = comments_list
		self._entry_id = entry_id
		self.comment_tree = []

	async def make_comment_tree(self):
		"""Алгоритм построения дерева комментариев с включением всех переданных комментариев."""
		try:
			self.all_comments.sort(key=lambda x: x.level, reverse=True)
			def get_index(comment_id, comments):
				for i in range(len(comments)):
					if comments[i].id == comment_id:
						return i
			for comment in self.all_comments:
				if (comment.reply_to != 0):
					next_index = get_index(comment.reply_to, self.all_comments)
					self.all_comments[next_index].answers.append(comment)
			comment_tree = [element for element in self.all_comments if element.level ==  0]
			self.comment_tree = comment_tree
			return comment_tree
		except Exception as e:
			_error(e)

	def get_comment_by_id(self, find_id:int):
		for comment in self.all_comments:
			if comment.id == find_id:
				return comment
		return None
	def get_comments_by_id(self, find_id:list):
		result = []
		for comment in self.all_comments:
			if comment.id in find_id:
				result.append(comment)
		return result
	
	def __repr__(self):
		return f"{self.__class__}: with entry_id {self.entry_id}"

	def __str__(self) -> str:
		result = ""
		for comment in self.all_comments:
			result += str(comment) + "\n"
		return result
        

class Comment:
    def __init__(self, id, auth_name, reply_to, text, lvl, date):
        self.id = id
        self.author_name = auth_name
        self.reply_to = reply_to
        self.text = text
        self.level = lvl
        self.time = date
        self.answers = []
    def __str__(self) -> str:
        """Trail version of this method"""
        return f"{self.author_name}: {self.text} <|endofstatement|>"
    
    def get_answers(self) -> list:
        return self.answers.copy()
    
    # def to_send(self):
    #     return {"text": f"{self._text}", "reply_to": f"{self._reply_to}","attachments": "[]"}
