import requests

email = "sergey.sysoev3010@gmail.com"
pswrd = "CheckPassword" 



data = {
    "values[email]":"sergey.sysoev3010@gmail.com",
    "values[password]": "CheckPassword",
    "mode": "raw"
}

# tip : https://gadjimuradov.ru/post/python-requests-avtorizaciya-na-sajte/
# tip2 : https://newtechaudit.ru/parsing-sajta-s-primeneniem-avtorizaczii/

class DTF:
	_url_login = 'https://api.dtf.ru/v3.0/auth/simple/login'
	_headers = {
    	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
	}

	def __init__(self, email, password):
		self.__session = requests.Session()
		self.__session.headers.update(self._headers)
		self.__combineData(email, password)
		response = self.__session.post(self._url_login, data=self.__sessionData)
		if response.json()['rc'] != 200:
			raise ConnectionError(response.text)
		else:
			print("Authorization is done.")

	def __combineData(self, email, password):
		self.__sessionData = {
    		"values[email]": email,
    		"values[password]": password,
    		"mode": "raw"
		}
	def find_all_posts_of_user_by_id(self, id):
		response = self.__session.get(f"https://dtf.ru/u/{id}")
		print(res)


dtf = DTF(email, pswrd)