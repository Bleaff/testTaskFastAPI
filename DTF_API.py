import requests

class DTF:
	def __init__(self, token):
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
		
	def get_all_my_entries(self):
		try:
			response = requests.get(self._url + "/user/me/entries", headers=self._header)
			return response
		except Exception as e:
			print(e)
			return None

	def get_comments_by_post_id(self, id, flag="popular"):
		try:
			response = requests.get(self._url + f"/entry/{id}/comments/{flag}", headers=self._header)
			return response
		except Exception as e:
			print(e)
			return None

	def get_new_comments(self):
		new_comments = dict()
		my_entries = [id_entry['id'] for id_entry in self.get_all_my_entries().json()['result']]
		for index, entry_id in enumerate(my_entries):
			new_comments[index] = {
				'entry_id': entry_id,
				'new_comments_tree': self.get_comments_by_post_id(entry_id, "recent").json()
			}
		return new_comments
	
	def __get_all_my_coms(self):
		try:
			response = requests.get(self._url + f"/user/me/comments", headers=self._header)
			coms_entries_id = {id['id']:id['entry']['id'] for id in response.json()['result']}
			return coms_entries_id
		except Exception as e:
			print(e)
			return None

	def __get_child_comment(self, parent_id, entry_id):
		try:
			all_comments_in_entry =  self.get_comments_by_post_id(entry_id).json()
			answers = [comment for comment in all_comments_in_entry['result'] if int(comment['replyTo']) == int(parent_id)]
			return answers
		except Exception as e:
			print(e)
			return None

	def __get_entry_by_comment_id(self, comment_id, author_id):
		try:
			response = requests.get(self._url + f"/user/{author_id}/comments", headers=self._header).json()
			for comment in response['result']:
				if comment_id == comment['id']:
					return comment['entry']['id']
			raise Exception("Entry not found! Try with another comment id!")
		except Exception as e:
			print(e)
			return None

	def get_answers_on_my_comments(self):
		try:
			replies = dict()
			com_to_entry_dict = self.__get_all_my_coms()
			for com_id in com_to_entry_dict.keys():
				 replies[int(com_id)] = self.__get_child_comment(com_id, com_to_entry_dict[com_id])
			return replies
		except Exception as e:
			print(e)
			return None

	def get_comment_tree(self, comment_id):
		try:
			response = requests.get(self._url + f"/comment/{comment_id}", headers=self._header).json()
			author_id = response['result']['author']['id']
			print(type(comment_id))
			entry_id = self.__get_entry_by_comment_id(int(comment_id), author_id)
			response = requests.get(self._url + f"/entry/{entry_id}/comments/thread/{comment_id}", headers=self._header).json()
			return response
		except Exception as e:
			print(e)
			return None
