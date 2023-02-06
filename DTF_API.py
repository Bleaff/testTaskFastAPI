import requests

class DTF:
	def __init__(self, token):
		self._token = token
		self._url = 'https://api.dtf.ru/v1.8'
		self._header = {'X-Device-Token': token}
		try:
			response = requests.get(self._url + '/user/me', headers=self._header)
		except Exception() as e:
			print(e)
		else:
			print("Connected successfuly!")
		
	def get_all_my_entries(self):
		try:
			response = requests.get(self._url + "/user/me/entries", headers=self._header)
			return response
		except Exception() as e:
			print(e)
			return None


	def get_comments_by_post_id(self, id, flag="popular"):
		try:
			response = requests.get(self._url + f"/entry/{id}/comments/{flag}", headers=self._header)
			return response
		except Exception() as e:
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


