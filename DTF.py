import requests
import aiohttp
from signalization import _error, _info
from Comment import Comment, CommentTree
import asyncio
import time
from random import randint
from Entry import *

class DTF:
	"""
	Класс для соединения с сервисом OsnovaApi (Tjournal, DTF, VC).
		Данный класс в автоматическом режиме получает набор комментариев на заданный список записей.
		Содержит методы, такие как: 
			Отправка комментариев в ответ.
			Получение списка новых комментариев.
			Построение дерева комментариев.
			Просмотр всех записей, принадлежащих пользователю с токеном 'token'.
	"""

	def __init__(self, token):
		"""Заполнение поля token, инициализация необходимых параметров."""
		self._token = token
		self._url = 'https://api.dtf.ru/v1.9'
		self._header = {'X-Device-Token': token}
		self.semaphore = asyncio.Semaphore(3)
		self.entries = []

	async def execute_response(self, query, repeat=False, query_path = ""):
		"""С использованием семафора ограничиваем время выполнения последовательных задач до минимального времени 0.33 сек на запрос"""
		async with self.semaphore:
			start = time.time()
			response = await self.get_query(query_path + query, repeat)
			if time.time() - start < 0.33:
				await asyncio.sleep(0.33 - time.time() + start)
			_info(f'[{start}]Time of request is {time.time() - start}')
			return response

	async def get_query(self, query, repeat=False):
		"""Search the web for a query""" 
		async with aiohttp.ClientSession(headers=self._header) as session: 
			async with session.get(self._url + query, ssl=False) as response:
				if response.status == requests.codes.ok: 
					data = await response.json()
					return data
				elif response.status == 401:
					_info("Unexpected troubles with the API-Key.")
				elif response.status == 500:
					if repeat != True:
						_info(f"Status code 500. Trying to request one more time.")
						return await self.do_query(query, repeat=True)
					else:
						_error(f"Impossible to get response. Status code 500.")
				else:
					_error(f"Status code is {response.status}")
					return None

	async def get_all_my_entries(self):
		"""Получение списка всех записей пользователя с токеном token"""
		# try:
		summarize = []
		response = await self.execute_response("/user/me/entries")
		for entry_json in response['result']:
			entry = Entry(entry_json)
			comments = await self.execute_response(f"/entry/{entry_json['id']}/comments")
			comments_list = [self._parse_comment(comment) for comment in comments['result']]
			com_tree = CommentTree(comments_list, entry.id)
			entry.set_comments(com_tree)
			self.add_to_follow(entry)
			summarize.append(entry.get_entry_as_dict())
		return summarize
		# except Exception as e:
		# 	_error(e)

	async def get_comments_by_post_id(self, id, flag="popular") -> CommentTree:
		"""Получение всех комментариев к записи с id записи в виде дерева."""
		try:
			response = await self.execute_response(f"/entry/{id}/comments/{flag}")
			all_comments =  [self._parse_comment(com) for com in response['result']]
			return CommentTree(all_comments, id)
		except Exception as e:
			_error(e)

	async def get_new_comments(self):
		"""Получение новых комментариев к записям пользователя с токеном token"""
		try:
			new_comments_dict = dict()
			count = await self.get_updates_count()
			print("Count of new event:",count)
			updates_list = await self.get_updates()
			entry_to_comment = self.parse_update(updates_list, 'comment', count)
			for entry in entry_to_comment:
				all_comments_from_entry = await self.get_comments_by_post_id(entry)
				comment_tree = all_comments_from_entry.get_comments_by_id(entry_to_comment[entry]) # получаем комментарии с нужными id из всех комментариев записи в виде CommentTree  
				new_comments_dict[entry] = comment_tree.get_all_comments_as_dict()
			return new_comments_dict
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
				answers[index] = self._parse_comment(el)
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
				replies_list = await self.__get_child_comment(com_id, com_to_entry_dict[com_id])
				replies[int(com_id)] = CommentTree(replies_list, -1).get_all_comments_as_dict()
			return replies
		except Exception as e:
			print(e)
			return None

	async def get_comment_tree(self, comment_id):
		"""
			Получение дерева комментариев (имея id комментария)
			Дерево строится  по ответам, принадлежащим одной ветке.
		"""
		try:
			start = time.time()
			response = await self.execute_response(f"/comment/{comment_id}")
			author_id = response['result']['author']['id']
			entry_id = await self.__get_entry_by_comment_id(int(comment_id), author_id)
			entry_text = await self.get_text_entry_by_id(entry_id)
			response =  await self.execute_response(f"/entry/{entry_id}/comments/thread/{comment_id}")
			all_comments = response['result']['items']
			for index, el in enumerate(all_comments):
				all_comments[index] = self._parse_comment(el)
			comment_tree = CommentTree(all_comments, entry_id)
			processed_comments = await comment_tree.make_comment_tree_v2(comment_id)
			processed_comments[0] = entry_text
			full = time.time() - start
			_info(f"Make Comment Tree method time:{full}")
			return processed_comments

		except Exception as e:
			_error(e)
			return None

	def _parse_comment(self, comment_json):
		"""Метод парсинга комментария с json в словарь"""
		try:
			comment = Comment(comment_json['id'],
								comment_json['author']['name'],
								comment_json['replyTo'],
								comment_json['text'],
								comment_json['level'],
								comment_json['date']
							)
			return comment
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
	
	async def get_updates(self):
		response = await self.execute_response("/user/me/updates?is_read=1")
		return response

	async def get_updates_count(self):
		response = await self.execute_response('/user/me/updates/count')
		return response['result']['count']

	def parse_update(self, json_updates:dict, type:str, count:int):
		"""type - может быть comment/reply/like_up"""
		data = json_updates['result']
		updates = {}
		entries = []
		comment_to_entry = {}

		for i in range(count):
			if data[i]['icon'] == type:
				splited_url = data[i]['url'].split('/')[5]
				entry_id = int(splited_url.split('-')[0])
				comment_id = int(splited_url.split('=')[-1])
				updates.setdefault(entry_id, list()).append(comment_id)
		return updates

	async def get_text_entry_by_id(self, entry_id:int)->str:
		""
		try:
			response = await self.execute_response(f"/entry/{entry_id}")
			parsed_entry = Entry(response['result'])
			result_str = f"{parsed_entry.title} {parsed_entry.intro}"
			return result_str
		except Exception as e:
			_error(e)

	# async def request_periodic_time(self):
	# 	while True:
	# 		wait_for = randint(50_000, 86_400) # Берем рандомное число секунд, через какое время начнут присылаться ответы на комментарии
	# 		await asyncio.sleep(wait_for)
	# 		updates = self.get_new_comments()

	def get_followed_entries(self)->list:
		"""
			Метод получения записей, отслеживаемые ботом
		"""
		res = [entr.get_entry_as_dict() for entr in self.entries]
		return res
	
	async def follow_entry(self, entry_id:int)->None:
		"""
			Метод добавления записи для отслеживания ботом
		"""
		try:
			entry_json = await self.execute_response(f"/entry/{entry_id}")
			comments = await self.execute_response(f"/entry/{entry_id}/comments")
			entry = Entry(entry_json['result'])
			comments_list = [self._parse_comment(comment) for comment in comments['result']]
			com_tree = CommentTree(comments_list, entry.id)
			entry.set_comments(com_tree)
			self.add_to_follow(entry)
		except Exception as e:
			_error(e)
		except TypeError as te:
			_error(f"Bad request was got:{e}")

	def add_to_follow(self, entr: Entry)->None:
		for entry in self.entries:
			if entr.id == entry.id:
				return 
		self.entries.append(entr) 







# Добавить методы отслеживания изменений записи
# Исправить метод получения новых комментариев
# Проверить работу set по удалению одинаковых записей из множеств