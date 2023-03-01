import requests
import aiohttp
from logging import * 

from DTF_parser import EntryParser

class DTF:
	def __init__(self, token):
		self.__EntryParser = EntryParser()
		self._token = token
		self._url = 'https://api.dtf.ru/v1.9'
		self._header = {'X-Device-Token': token}

	async def execute_response(self, query, repeat=False):
		"""Search the web for a query""" 
		async with aiohttp.ClientSession(headers=self._header) as session: 
			async with session.get(self._url + query) as response:
				if response.status_code == requests.codes.ok: 
					data = await response.json()
					return data
				elif response.status_code == 401:
					_info("Unexpected troubles with the API-Key.")
				elif response.status_code == 500:
					if repeat != True:
						_info(f"Status code 500. Trying to request one more time.")
						self.execute_response(query, repeat=True)
					else:
						_error(f"Impossible to get response. Status code 500.")
				else:
					_error(f"Status code is {response.status_code}")
					return None

	async def get_all_my_entries(self):
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
		try:
			response = await self.execute_response(f"/entry/{id}/comments/{flag}")
			all_comments =  [await self.__pars_comment(com) for com in response['result']]
			comment_tree = await self.make_comment_tree(all_comments)
			return comment_tree
		except Exception as e:
			_error(e)

	async def get_new_comments(self):
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
		try:
			response = await self.execute_response(f"/user/me/comments")
			coms_entries_id = {id['id']:id['entry']['id'] for id in response['result']}
			return coms_entries_id
		except Exception as e:
			_error(e)

	async def __get_child_comment(self, parent_id, entry_id):
		try:
			all_comments_in_entry = await self.execute_response(f"/entry/{entry_id}/comments/popular")
			answers = [comment for comment in all_comments_in_entry['result'] if int(comment['replyTo']) == int(parent_id)]
			for index, el in enumerate(answers):
				answers[index] = await self.__pars_comment(el)
			return answers
		except Exception as e:
			_error(e)

	async def __get_entry_by_comment_id(self, comment_id, author_id):
		try:
			response = await self.execute_response(f"/user/{author_id}/comments")
			for comment in response['result']:
				if comment_id == comment['id']:
					return comment['entry']['id']
			raise Exception("Entry not found! Try with another comment id!")
		except Exception as e:
			_error(e)

	async def get_answers_on_my_comments(self):
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
