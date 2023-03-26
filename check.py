a = [
    {
        "id": 1,
        "author_name": "Syhapod",
        "reply_to": 0,
        "text": "В полигон иди, тебе уже кидали",
        "level": 0,
        "time": 1675664948,
        "answers": []
      },
      {
        "id": 2,
        "author_name": "Котьмак из школы кота",
        "reply_to": 0,
        "text": "Дарю:",
        "level": 0,
        "time": 1675668258,
        "answers": []
      },
      {
        "id": 3,
        "author_name": "Котьмак из школы кота",
        "reply_to": 22485169,
        "text": "И в общей ленте не мусоришь, и за тем куда постишь следить не надо, и от лишних телодвижений по занесению тебя в чс окружающих избавляешь\nСплошные плюсы",
        "level": 1,
        "time": 1675668332,
        "answers": []
      },
      {
        "id": 4,
        "author_name": "Artem Glechinsky",
        "reply_to": 0,
        "text": "zczxc",
        "level": 0,
        "time": 1678118312,
        "answers": []
      }
    ]

b = [
    {
        "id": 1,
        "author_name": "Syhapod",
        "reply_to": 0,
        "text": "В полигон иди, тебе уже кидали",
        "level": 0,
        "time": 1675664948,
        "answers": []
      },
      {
        "id": 2,
        "author_name": "Котьмак из школы кота",
        "reply_to": 0,
        "text": "Дарю:",
        "level": 0,
        "time": 1675668258,
        "answers": []
      },
      {
        "id": 3,
        "author_name": "Котьмак из школы кота",
        "reply_to": 22485169,
        "text": "И в общей ленте не мусоришь, и за тем куда постишь следить не надо, и от лишних телодвижений по занесению тебя в чс окружающих избавляешь\nСплошные плюсы",
        "level": 1,
        "time": 1675668332,
        "answers": []
      },
      {
        "id": 4,
        "author_name": "Artem Glechinsky",
        "reply_to": 0,
        "text": "call of duty",
        "level": 0,
        "time": 1678118312,
        "answers": []
      },
      {
        "id": 5,
        "author_name": "Artem Glechinsky",
        "reply_to": 0,
        "text": "call of duty",
        "level": 0,
        "time": 1678118312,
        "answers": []
      }
      ,
      {
        "id": 6,
        "author_name": "Artem Glechinsky",
        "reply_to": 0,
        "text": "call of duty",
        "level": 0,
        "time": 1678118312,
        "answers": []
      }
    ]

# set_a, set_b = set(a), set(b)
# diff = set_a - set_b
lst_a = [el ["id"] for el in a]
lst_b = [el ["id"] for el in b]

set_a, set_b = set(lst_a), set(lst_b)
print(set_a)
print(set_b)
diff = set_b - set_a
print(diff)