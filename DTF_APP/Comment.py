from signalization import _error
from math import ceil
from random import choices

class Comment:
	"""Класс комментария, содержащий поля id, имя автора, на какой комментарий является ответом текущий комментарий, текст комментария, уровень вложенности и дату"""
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

	def get_reply(self):
		"""Метод возвращает id комментария, ответом на который ялвяется текущий коммент"""
		return  self.reply_to
	
	def get_text(self) -> str:
		return self.text

class CommentTree:
	"""
		Класс для удобства взаимодействия с комментариями одной записи. Может использоваться для вывода все комментарикв в виде беседы, 
		построения дерева комментариев.
	"""
	def __init__(self, comments_list :list, entry_id :int) -> None:
		"""Инициализация дерева комментариев параметрами: 
			1. Список комментариев - comment_list
			2. id записи - entry_id
		"""
		self.all_comments = comments_list
		self.entry_id = entry_id
		self.comment_tree = []
		self.list_of_id = []

	async def make_comment_tree(self, comment_id)->list:
		"""Алгоритм построения остортированного списка комментариев вверх от переданного comment_id."""
		try:
			list_of_comments = self.get_all_comments()
			list_of_comments.sort(key=lambda x: x.level, reverse=True)
			def get_index(comment_id, comments):
				for i in range(len(comments)):
					if comments[i].id == comment_id:
						return i
			for comment in list_of_comments:
				if (comment.reply_to != 0):
					next_index = get_index(comment.reply_to, list_of_comments)
					list_of_comments[next_index].answers.append(comment)
			comment_tree = [element for element in list_of_comments if element.level ==  0]
			self.comment_tree = comment_tree
			return comment_tree
		except Exception as e:
			_error(e)
	
	async def make_comment_tree_v2(self, comment_id) -> list[str]:
	#FIXME ????
		"""Алгоритм построения остортированного списка комментариев вверх от переданного comment_id.
		Возвращаемое значение: list = [пост_id, 'коммент1', 'коммент2'...]"""
		last_comment = self.get_comment_by_id(comment_id)
		result_list = [last_comment.text, last_comment.author_name] # Обратный порядок, т.к. далее разворачиваем список
		next_comment = self.get_next_comment(comment_id)
		while (next_comment):
			result_list.append(next_comment.text)
			result_list.append(next_comment.author_name)
			next_comment = self.get_next_comment(next_comment)
		result_list.append(self.entry_id)
		result_list.reverse()
		return result_list

	def get_comment_by_id(self, find_id:int) -> Comment:
		temp = int(find_id)
		find_id = temp
		for comment in self.all_comments:
			if comment.id == find_id:
				return comment
		return None

	def get_comments_by_id(self, find_id:list):
		"""Return value -> CommentTree"""
		result = []
		for comment in self.all_comments:
			if comment.id in find_id:
				result.append(comment)
		return CommentTree(result, self.entry_id)
	
	def __repr__(self)->str:
		return f"{self.__class__}: with entry_id {self.entry_id}"

	def __str__(self) -> str:
		result = ""
		for comment in self.all_comments:
			result += str(comment) + "\n"
		return result

	def get_all_comments(self)->list:
		return self.all_comments.copy()

	def get_all_comments_as_dict(self)->dict:
		result = []
		for comment in self.all_comments:
				result.append(comment.__dict__)
		return result

	def get_comment_tree_as_dict(self)->dict:
		result = []
		for comment in self.comment_tree:
				result.append(comment.__dict__)
		return result
	
	def get_tree_as_str(self)->str:
		result = ""
		for comment in self.comment_tree:
			result += str(comment) + "\n"
		return result

	def get_next_comment(self, cur_comment)->Comment:
		"""Движение от последнего комментария наверх"""
		if isinstance(cur_comment, Comment):
			return self.get_comment_by_id(cur_comment.get_reply())
		else:
			curent_comment = self.get_comment_by_id(cur_comment)
			return self.get_comment_by_id(curent_comment.get_reply())
	
	def get_n_percent(self, n=40):
		"""Возвращает список n% от всех имеющихся в CommentTree комментариев"""
		size_of_n = ceil(len(self) * n / 100)
		choosen =  choices(self.all_comments, k=size_of_n)
		return CommentTree(choosen, self.entry_id)
	
	def get_comments_without_author(self, author_name):
		comments_without_author = []
		for comment in self.all_comments:
			if author_name != comment.author_name:
				comments_without_author.append(comment)
		return CommentTree(comments_without_author, self.entry_id)
	
	def get_comments_with_author(self, author_name):
		comments_with_author = []
		for comment in self.all_comments:
			if author_name == comment.author_name:
				comments_with_author.append(comment)
		return CommentTree(comments_with_author, self.entry_id)
	
	def get_all_comments_reply_as_set(self):
		return set([comment.reply_to for comment in self.all_comments])

	def get_all_comments_id_as_set(self):
		return set([comment.id for comment in self.all_comments])

	def __len__(self):
		return len(self.all_comments)
