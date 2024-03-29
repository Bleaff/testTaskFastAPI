import requests
import aiohttp
import json
from signalization import _error, _info, _success
from Comment import Comment, CommentTree
import asyncio
import time
from random import randint
from Entry import *
from api_models import *
from BD_connection_module import DataBaseConn

class OsnovaApiConn:
	"""
	Класс для соединения с сервисом OsnovaApi (Tjournal, DTF, VC).
		Данный класс в автоматическом режиме получает набор комментариев на заданный список записей.
		Содержит методы, такие как: 
			Отправка комментариев в ответ.
			Получение списка новых комментариев.
			Построение дерева комментариев.
			Просмотр всех записей, принадлежащих пользователю с токеном 'token'.
	"""

	def __init__(self, token, pretext, bd_id, advertising_id, place = "dtf"):
		"""Заполнение поля token, инициализация необходимых параметров."""
		self.id = bd_id
		self._token = token
		self._url = f'https://api.{place}.ru/v1.9'
		self._header = {'X-Device-Token': token}
		self.advertising_id = advertising_id
		self.semaphore = asyncio.Semaphore(3)
		self.entries = []
		self.answers_rate = 30
		self.is_active = False
		self.active_task = None # Parameter for endless cycle task (request periodic time method)
		self.pretext = pretext
		self.temperature = 1
		self.top_p = 1
		self.model = 'gpt-3.5-turbo'
		self.model_url = "http://0.0.0.0:35000/generate_comment"
		self.db_conn = DataBaseConn()

	async def execute_response(self, query, repeat=False, query_path = ""):
		"""С использованием семафора ограничиваем время выполнения последовательных задач до минимального времени 0.33 сек на запрос"""
		async with self.semaphore:
			start = time.time()
			response = await self.get_query(query_path + query, repeat)
			if time.time() - start < 0.33:
				await asyncio.sleep(0.33 - time.time() + start)
			# _info(f'[{start}]Time of request is {time.time() - start}')
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
		try:
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
		except Exception as e:
			_error(e)

	async def get_comments_by_post_id(self, id, flag="popular") -> CommentTree:
		"""Получение всех комментариев к записи с id записи в виде дерева."""
		try:
			response = await self.execute_response(f"/entry/{id}/comments/{flag}")
			all_comments =  [self._parse_comment(com) for com in response['result']]
			return CommentTree(all_comments, id)
		except Exception as e:
			_error(e)

	async def get_replies(self):
		"""Получение новых ответов на свои комментарии.
			Возвращаемое значение: [(Entry1, CommentTree), (Entry2, CommentTree), ...], где у EntryN в параметре marked_comments лежат ответы на сообщение пользователя."""
		try:
			new_comments_dict = []
			count = await self.get_updates_count()
			_info(f"    B#{self.id} {self.user_name}:Count of new replies:{count}")
			if not count:
				return [] 
			updates_list = await self.get_updates()
			entry_to_comment = self.parse_update(updates_list, 'reply', count)
			for entry_id in entry_to_comment:
				entry = await self.get_full_entry(int(entry_id))
				entry.marked_comments = entry.comments.get_comments_by_id(entry_to_comment[entry_id]) # получаем комментарии с нужными id из всех комментариев записи в виде CommentTree  
				new_comments_dict.append((entry, entry.marked_comments))
			
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
			# _info(f"Make Comment Tree method time:{full}")
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

	async def send_post_response(self, data): # Now is only for replies to comments
		async with aiohttp.ClientSession(headers=self._header) as session: 
			async with session.post(self._url + "/comment/add", data=data) as response:
				if response.status == requests.codes.ok: 
					data = await response.json()
					return data
				elif response.status == 401:
					_info("Unexpected troubles with the API-Key.")
				else:
					_error(f"Status code is {response.status}")
					return None

	async def reply_to_comment(self, entry_id:int, reply_to:int, msg:str):
		"""
			Метод отправки ответа на комментарий или на запись с entry_id. 
			ВНИМАНИЕ:Entry_id является обязательным параметром, даже при ответе на комментарий.
		"""
		template = {
  					"id": f"{int(entry_id)}",
  					"text": f"{msg}",
  					"reply_to": f"{reply_to}",
  					"attachments": "[]"
					}
		if entry_id == 0:
			return _error("Invalid entry id. Entry id is a required parameter!")
		async with self.semaphore:
			start = time.time()
			response = await self.send_post_response(template)
			if time.time() - start < 20:
				await asyncio.sleep(20 - time.time() + start)
			# _info(f'[{start}]Time of request is {time.time() - start}')
			return response

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

	def produce_singularity(self, entry_comment, entry_reply):
		# Метод для удаления дубликатов из отправляющего пула. В методе объединяются комментарии для ответа модели в один пул.
		for i, pair in enumerate(entry_comment):
			for entry in entry_reply: # entry looks like: (entry, commentTree)
				if pair[0].id == entry[0].id:
					entry_comment[i][0].marked_comments = entry[0].marked_comments
		#marked_comment - комментарии, которые являются ответом на наши комментарии
		for i, pair in enumerate(entry_comment):
			if not pair[0].marked_comments:
				continue
			common_set = pair[0].marked_comments.get_all_comments_id_as_set().union(pair[1].get_all_comments_id_as_set())
			entry_comment[i] = (pair[0], pair[0].comments.get_comments_by_id(list(common_set)))
		if not len(entry_comment) and len(entry_reply): #Если нет новых комментариев к записи, но есть ответы, мы отвечаем.
			entry_comment = entry_reply
		return entry_comment

	async def auto_reply_to_comment(self, updates, replies):
		"""Метод для выполнения действий по автоматическому ответу на комментарии к посту."""
		choosen = self.produce_singularity(updates, replies) # Сначала сливаем все в один пул (комменты и ответы)
		choosen = await self.get_n_part_from_new_pool(self.answers_rate, choosen) # Далее из пула выбираем рандомную часть для ответа
		await self.configure_and_send(choosen, "FROM COMMENT")
	
	async def auto_reply_to_replies(self):
		try:
			new_replies = await self.get_replies()
			if len(new_replies) == 0:
				return []
			return new_replies
		except Exception as e:
			_error(e)

	async def configure_and_send(self, entry_to_comtree, from_f):
		"""Метод собирает в один контейнер в необходимом формате данные, отправляет их и принимает обратно.
			Также здесь происходит ответ на полученные ответы."""
		data = await self.send_to_model(entry_to_comtree) #Формируем данные для отправки в модель
		rest_tokens = await self.db_conn.get_rest_token(self.advertising_id)
		if rest_tokens <= 0:
			_info(f"Bot #{self.id}: Bot becomes inactive due to low token balance!")
			self.cancel_my_task()
		response = await self.post_to_model(data, self.model_url) #Получили ответ от модели, далее отвечаем на комменты
		#FIXME add if resp["replies"][i]["reply"] != 'ERROR' - удалять из ответов и не списывать токен
		if response is None:
			_error("Something went wrong!")
		for entry in response['replies']: #Ответили на полученные комменты
			for answer in entry['CommentTrees']:
				await self.reply_to_comment(entry["entry_id"], answer['comment_id'], answer['reply'])

	async def request_periodic_time(self):
		"""Метод с заданной периодичностью посылает запросы на osnovaAPI, для обновления данных об отслеживаемых записях. 
			В данном методе запускается весь цикл от получения обновлений, до отправки ответа выбранным комментам."""
		while True:
			wait_for = randint(20, 45) # Берем рандомное число секунд, через какое время начнут присылаться ответы на комментарии
			await asyncio.sleep(wait_for)
			_info(f'    B#{self.id} {self.user_name}: Wait for:{wait_for}')
			updates = await self.update_followed_entries()
			replies = await self.auto_reply_to_replies()
			if (updates and  len(updates)) or len(replies):
				await self.auto_reply_to_comment(updates, replies)
			
			else:
				_info(f'    B#{self.id} {self.user_name}: Nothing to update.')

	async def post_to_model(self, data, model_url):
		async with aiohttp.ClientSession() as session: 
			async with session.post(json=data, url=model_url) as response:
				if response.status == requests.codes.ok: 
					data = await response.json()
					return data
				else:
					_error(await response.text())
					return None

	def get_followed_entries(self)->list:
		"""
			Метод получения записей, отслеживаемые ботом
		"""
		res = [entr.get_entry_as_dict() for entr in self.entries]
		return res
	
	async def get_full_entry(self, entry_id):
		"""Метод получения информации о записи и возврат сформированной записи с переданным id."""
		try:
			entry_json = await self.execute_response(f"/entry/{entry_id}")
			comments = await self.execute_response(f"/entry/{entry_id}/comments")
			entry = Entry(entry_json['result'])
			comments_list = [self._parse_comment(comment) for comment in comments['result']]
			com_tree = CommentTree(comments_list, entry.id)
			entry.set_comments(com_tree)
			return entry
		except Exception as e:
			_error(e)

	async def follow_entry(self, entry_id:int)->None:
		"""
			Метод добавления записи для отслеживания ботом
		"""
		try:
			entry = await self.get_full_entry(entry_id)
			self.add_to_follow(entry)
		except TypeError as te:
			_error(f"Bad request was got:{e}")
		except Exception as e:
			_error(e)

	def add_to_follow(self, entr: Entry)->None:
		for entry in self.entries:
			if entr.id == entry.id:
				return 
		self.entries.append(entr) 

	async def update_followed_entries(self)->list:
		"""Обновление записей, находящихся в списке на обновлнение (self.entries).
			Метод возвращает список пар (NewEntry, NewCommentTree), где NewCommentTree с исключительно новыми комментариями (не полный набор комментариев)"""
		new_comments_pool = []
		for i, old_entry in enumerate(self.entries):
			new_entry = await self.get_full_entry(old_entry.id)
			if new_entry.comments_count == old_entry.comments_count:
				continue														#Избавляемся от проверок, в случае остсутствия новых комментариев
			new_comments_pool.append((new_entry, old_entry.set_updates(new_entry))) # получаем список новых комментариев, запечатанных в Entry
		return new_comments_pool
	
	async def get_n_part_from_new_pool(self, n:int, new_pool : list)->list:
		"""Отбор n% комментариев из числа новых комментариев.
			new_pool -> [(entry,comment_tree), (entry,comment_tree), (entry,comment_tree)]
			Метод возвращает список пар (Entry, NewCommentTree), где NewCommentTree с исключительно новыми комментариями (не полный набор комментариев)"""
		#FIXME удобен для запуска в отдельный поток
		choosen_comments = []

		for entry, com_tree in new_pool:
			new_com_tree = com_tree.get_n_percent(n)
			choosen_comments.append((entry, new_com_tree))

		return choosen_comments
	
	async def send_to_model(self,to_send:list)->list:
		"""Метод принимает на вход список пар (Entry, CommentTree) с новыми значениями комментариев
			Возвращаемое значение для каждой пары  (Entry, CommentTree):
				[[username: post, username:comment, username:comment, ... ], ..., []]"""
		to_send_list = []
		for entry, com_tree in to_send:
			entry_dict = {"entry_id": str(entry.id), "CommentTrees": []}
			all_com = com_tree.get_all_comments()
			for comment in all_com: #Строим для каждого комментария из выбранных свою цепочку 
				tree = await entry.comments.make_comment_tree_v2(comment.id)
				if len(tree):
					tree[0] = entry.auth_name
					tree.insert(1, str(entry))
				entry_dict["CommentTrees"].append({"comment_id": str(comment.id), "CommentTree": tree})
			to_send_list.append(entry_dict)
		result = {"entries":to_send_list}
		result['pretext'] = self.pretext
		result['temperature'] = self.temperature
		result['nickname'] = self.user_name
		result['top_p'] = self.top_p
		result['model'] = self.model
		print(result)
		return result
	
	async def run_setup(self):
		"""
			Метод для первого запуска в обычном режиме(прослушивания записей) + выставление собственных записей в список прослушивания.
		"""
		response = await self.execute_response('/user/me')
		if not response:
			_error('Bot', self.user_name,"An error occurred while retrieving data")
			return None
		self.user_id = response["result"]['id']
		self.user_name = response['result']['name']
		await self.get_all_my_entries()
		_success('Bot', self.user_name, 'started')

	async def start_my_task(self):
		if not self.is_active:
			self.active_task = asyncio.create_task(self.request_periodic_time())
			self.is_active = True

	async def cancel_my_task(self):
		if self.is_active:
			status = self.active_task.cancel()
			_info(f'Bot #{self.id} has canceled his task status:{status}')
			while True:
				await asyncio.sleep(0.3)
				if self.active_task.cancelled():
					_info(f'Bot #{self.id} has canceled his task status:{status}')
					break
			self.is_active = False
			self.active_task = None
	
	async def enterance_into_foreign_entry(self, *entry_id_or_ids):
		# Получаем все комментарии исследуемой записи, выбираем из них часть
		entry_list = []
		try:
			for entry_id in entry_id_or_ids:
				entry = await self.get_full_entry(entry_id)
				entry_list.append((entry, entry.comments))
			choosen_comments = await self.get_n_part_from_new_pool(self.answers_rate, entry_list)
			await self.configure_and_send(choosen_comments, "FROM SINGLE ENTRANCE")
		except Exception as e:
			_error(e)
