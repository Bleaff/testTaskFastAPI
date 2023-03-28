import requests

data = """{
    {
        'entry_id': 1612676,
        'CommentTrees': 
            [
                (23828003, 
                [('Серёжа Сысоев', 'Ипользуя библиотеку requestsЭтап авторизации + запрос пройден'), 
                 ('Artem Glechinsky', 'Новый коммент!_Ц()'),
                 ('Artem Glechinsky', 'Круто!'), 
                 ('Artem Glechinsky', 'Шиук!')])
            ]
    }, 
    {
        'entry_id': 1612527, 
        'CommentTrees': 
            [(23827992, 
                [('Серёжа Сысоев', 'Первые шажки по парсу dtf.Hello world'), 
                 ('Artem Glechinsky', 'qweqweq'), 
                 ('Artem Glechinsky', 'sa'), 
                 ('Artem Glechinsky', 'da'), 
                 ('Artem Glechinsky', 'два уоммент')])
            ]
    }
}"""

res = requests.post("http://127.0.0.1:8000/generate_comment", data=data)
print(res)

