import requests
from DTF_parser import EntryParser

class DTF:
	def __init__(self, token):
		self.__EntryParser = EntryParser()
		self._token = token
		self._url = 'https://api.dtf.ru/v1.9'
		self._header = {'X-Device-Token': token}
		try:
			response = requests.get(self._url + '/user/me', headers=self._header)
			self._user_id = response.json()['result']['id']
		except Exception as e:
			print(e)
		else:
			print("Connected successfuly!")
		
	async def get_all_my_entries(self):
		try:
			summarize = {'message':[]}
			response = requests.get(self._url + "/user/me/entries", headers=self._header).json()
			for entry in response['result']:
				comments = requests.get(self._url + f"/entry/{entry['id']}/comments", headers=self._header).json()
				comments_id = {id['id'] for id in comments['result']}
				summarize['message'].append(self.__EntryParser.parse_entry(entry, comments_id))
			return summarize
		except Exception as e:
			print(e)
			return None

	async def get_comments_by_post_id(self, id, flag="popular"):
		try:
			response = requests.get(self._url + f"/entry/{id}/comments/{flag}", headers=self._header).json()
			all_comments =  [await self.__pars_comment(com) for com in response['result']]
			comment_tree = await self.make_comment_tree(all_comments)
			return comment_tree
		except Exception as e:
			print(e)
			return None

	async def get_new_comments(self):
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
	
	async def __get_all_my_coms(self):
		try:
			response = requests.get(self._url + f"/user/me/comments", headers=self._header)
			coms_entries_id = {id['id']:id['entry']['id'] for id in response.json()['result']}
			return coms_entries_id
		except Exception as e:
			print(e)
			return None

	async def __get_child_comment(self, parent_id, entry_id):
		try:
			all_comments_in_entry =  await self.get_comments_by_post_id(entry_id)
			print(all_comments_in_entry)
			answers = [comment for comment in all_comments_in_entry if int(comment['reply_to']) == int(parent_id)]
			print(f"_______________________________{parent_id}_________________________________________\n{answers}")
			return answers
		except Exception as e:
			print(e)
			return None

	async def __get_entry_by_comment_id(self, comment_id, author_id):
		try:
			response = requests.get(self._url + f"/user/{author_id}/comments", headers=self._header).json()
			for comment in response['result']:
				if comment_id == comment['id']:
					return comment['entry']['id']
			raise Exception("Entry not found! Try with another comment id!")
		except Exception as e:
			print(e)
			return None

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
			response = requests.get(self._url + f"/comment/{comment_id}", headers=self._header).json()
			author_id = response['result']['author']['id']
			print(type(comment_id))
			entry_id = await self.__get_entry_by_comment_id(int(comment_id), author_id)
			print(entry_id)
			response = requests.get(self._url + f"/entry/{entry_id}/comments/thread/{comment_id}", headers=self._header).json()
			return response
		except Exception as e:
			print(e)
			return None

	async def __pars_comment(self, comment_json):
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

	async def make_comment_tree(self, all_comments):

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

