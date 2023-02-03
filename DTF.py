import requests

email = "sergey.sysoev3010@gmail.com"
pswrd = "CheckPassword" 

url_login = 'https://api.dtf.ru/v3.0/auth/simple/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
}

# tip : https://gadjimuradov.ru/post/python-requests-avtorizaciya-na-sajte/
# tip2 : https://newtechaudit.ru/parsing-sajta-s-primeneniem-avtorizaczii/

class DTF:
	def __init__(self):
		

    def __make_request(self):
		