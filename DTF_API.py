import requests
import aiohttp
from signalization import _error, _info
from comment import Comment




from DTF_parser import EntryParser

class DTF:
	"""
	Класс для соединения с сервисом OsnovaApi (Tjournal, DTF, VC).
		Данный класс предоставляет методы взаимодействия с сервисом DTF.
		Поддерживает такие методы как:
			Отправка комментариев в ответ.
			Получение списка новых комментариев.
			Построение дерева комментариев.
			Просмотр всех записей, принадлежащих пользователю с токеном 'token'.
	"""
	def __init__(self, token):
		"""Заполнение поля token, инициализация необходимых параметров."""
		self.__EntryParser = EntryParser()
		self._token = token
		self._url = 'https://api.dtf.ru/v1.9'
		self._header = {'X-Device-Token': token}

	async def execute_response(self, query, repeat=False):
		"""Search the web for a query""" 
		async with aiohttp.ClientSession(headers=self._header) as session: 
			async with session.get(self._url + query) as response:
				if response.status == requests.codes.ok: 
					data = await response.json()
					return data
				elif response.status == 401:
					_info("Unexpected troubles with the API-Key.")
				elif response.status == 500:
					if repeat != True:
						_info(f"Status code 500. Trying to request one more time.")
						self.execute_response(query, repeat=True)
					else:
						_error(f"Impossible to get response. Status code 500.")
				else:
					_error(f"Status code is {response.status}")
					return None

	async def get_all_my_entries(self):
		"""Получение списка всех записей пользователя с токеном token"""
		try:
			summarize = {'message':[]}
			response = await self.execute_response("/user/me/entries")
			for entry in response['result']:
				comments = requests.get(self._url + f"/entry/{entry['id']}/comments", headers=self._header).json()
				comments_id = {id['id'] for id in comments['result']}
				summarize['message'].append(self.__EntryParser.parse_entry(entry, comments_id))
			return summarize
		except Exception as e:
			_error(e)


	async def get_comments_by_post_id(self, id, flag="popular"):
		"""Получение всех комментариев к записи с id записи"""
		try:
			response = await self.execute_response(f"/entry/{id}/comments/{flag}")
			all_comments =  [await self.__pars_comment(com) for com in response['result']]
			comment_tree = await self.make_comment_tree(all_comments)
			return comment_tree
		except Exception as e:
			_error(e)

	async def get_new_comments(self):
		"""Получение новых комментариев к записям пользователя с токеном token"""
		try:
			new_comments = dict()
			ans = await self.get_all_my_entries()
			print(ans)
			my_entries = [id_entry['id'] for id_entry in ans['message']]
			for index, entry_id in enumerate(my_entries):
				new_comments[index] = {
					'entry_id': entry_id,
					'new_comments_tree': await self.get_comments_by_post_id(entry_id, "recent")
				}
			return new_comments
		except Exception as e:
			_error(e)
	
	async def __get_all_my_coms(self):
		"""Приватный метод для получения всех своих комментариев"""
		try:
			response = await self.execute_response(f"/user/me/comments")
			coms_entries_id = {id['id']:id['entry']['id'] for id in response['result']}
			return coms_entries_id
		except Exception as e:
			_error(e)

	async def __get_child_comment(self, parent_id, entry_id):
		"""Метод получения всех ответов на комментарий parent_id в записи entry_id"""
		try:
			all_comments_in_entry = await self.execute_response(f"/entry/{entry_id}/comments/popular")
			answers = [comment for comment in all_comments_in_entry['result'] if int(comment['replyTo']) == int(parent_id)]
			for index, el in enumerate(answers):
				answers[index] = await self.__pars_comment(el)
			return answers
		except Exception as e:
			_error(e)

	async def __get_entry_by_comment_id(self, comment_id, author_id):
		"""Получение entry_id записи по id комментария и id автора"""
		try:
			response = await self.execute_response(f"/user/{author_id}/comments")
			for comment in response['result']:
				if comment_id == comment['id']:
					return comment['entry']['id']
			raise Exception("Entry not found! Try with another comment id!")
		except Exception as e:
			_error(e)

	async def get_answers_on_my_comments(self):
		"""Получение ответов на все свои комментарии"""
		try:
			replies = dict()
			com_to_entry_dict = await self.__get_all_my_coms()
			for com_id in com_to_entry_dict.keys():
				replies[int(com_id)] = await self.__get_child_comment(com_id, com_to_entry_dict[com_id])
			return replies
		except Exception as e:
			print(e)
			return None

	async def get_comment_tree(self, comment_id):
		"""
			Получение дерева комментариев (имея id комментария)
			Дерево строится с включением всех комментариев, принадлежащих одной ветке.
		"""
		try:
			response = await self.execute_response(f"/comment/{comment_id}")
			author_id = response['result']['author']['id']
			entry_id = await self.__get_entry_by_comment_id(int(comment_id), author_id)
			response =  await self.execute_response(f"/entry/{entry_id}/comments/thread/{comment_id}")
			all_comments = response['result']['items']
			for index, el in enumerate(all_comments):
				all_comments[index] = await self.__pars_comment(el)
			return await self.make_comment_tree(all_comments)
		except Exception as e:
			print(e)
			return None

	async def __pars_comment(self, comment_json):
		"""Метод парсинга комментария с json в словарь"""
		try:
			result = dict()
			result["id"] = comment_json['id']
			result['author_name'] = comment_json['author']['name']
			result['media'] = comment_json['media']
			result['reply_to'] = comment_json['replyTo']
			result['text'] = comment_json['text']
			result['level'] = comment_json['level']
			result['attaches'] = []
			for attach in comment_json['attaches']:
				if attach['type'] == 'link':
					result['attaches'].append(self.__EntryParser.link_parser__(attach))
			result['answers'] = []
			return result
		except Exception as e:
			_error(e)

	async def make_comment_tree(self, all_comments):
		"""Алгоритм построения дерева комментариев с включением всех комментариев одной ветки"""
		try:
			all_comments.sort(key=lambda x: x['level'], reverse=True)
			def get_index(comment_id, comments):
				for i in range(len(comments)):
					if comments[i]['id'] == comment_id:
						return i
			for comment in all_comments:
				if (comment['reply_to'] != 0):
					next_index = get_index(comment['reply_to'], all_comments)
					all_comments[next_index]['answers'].append(comment)
			comment_tree = [element for element in all_comments if element['level'] ==  0]
			return comment_tree
		except Exception as e:
			_error(e)

	async def reply_to_comment(self, entry_id:int, reply_to:int, msg:str):
		"""
			Метод отправки ответа на комментарий или на запись с entry_id. 
			ВНИМАНИЕ:Entry_id является обязательным параметром, даже при ответе на комментарий.
		"""
		template = {
  					"id": f"{entry_id}",
  					"text": f"{msg}",
  					"reply_to": f"{reply_to}",
  					"attachments": "[]"
					}
		if entry_id == 0:
			return _error("Invalid entry id. Entry id is a required parameter!")
		async with aiohttp.ClientSession(headers=self._header) as session: 
			async with session.post(self._url + "/comment/add", data=template) as response:
				if response.status == requests.codes.ok: 
					data = await response.json()
					return data
				elif response.status == 401:
					_info("Unexpected troubles with the API-Key.")
				else:
					_error(f"Status code is {response.status}")
					return None
	
	async def send_to_model(comment:Comment):
		#FIXME method 
		"""
			Метод для отправки в модель дерева комментариев.
			Так как метод еще не дописан(не продумана система отправки) шаблон будет следующим.
		"""
		async with aiohttp.ClientSession(headers=self._header) as session: 
			async with session.post(self._url + "/comment/add", data=template) as response:
				if response.status == requests.codes.ok: 
					data = await response.json()
					return data
				elif response.status == 401:
					_info("Unexpected troubles with the API-Key.")
				else:
					_error(f"Status code is {response.status}")
					return None
# FIXME IDEA: использовать HTTPException для возврата клиенту кода ошибки. Но на сколько это нужно?¿