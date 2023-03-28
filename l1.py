import requests
import json
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

#СТРОКИ 30, 31 - dict comprehensions, строка 29 - пример списка
lis1 = [{'entry_id': 1612676, 'CommentTrees': [(23888912, [('Серёжа Сысоев', 'Ипользуя библиотеку requests Этап авторизации + запрос пройден'), ('Artem Glechinsky', 'И тут'), ('Серёжа Сысоев', 'answer_from_model'), ('Artem Glechinsky', 'Here!'), ('Серёжа Сысоев', 'Deep thought...'), ('Vlad Dremov', 'deeper thought')]), (23888918, [('Серёжа Сысоев', 'Ипользуя библиотеку requests Этап авторизации + запрос пройден'), ('Artem Glechinsky', 'И тут'), ('Серёжа Сысоев', 'answer_from_model'), ('Artem Glechinsky', 'Here!'), ('Серёжа Сысоев', 'Deep thought...'), ('Vlad Dremov', '123')])]}]
lis2 = {lis1[i]['CommentTrees'][j][0]: lis1[i]['CommentTrees'][j][1] for i in range(len(lis1)) for j in range(len(lis1[i]['CommentTrees']))}
print(lis2)
lis3 = {k: [item for t in v for item in t] for k,v in lis2.items() }
print(lis3)
