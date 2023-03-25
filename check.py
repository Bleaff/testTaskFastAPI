a = [
    {
        "id": 22484013,
        "author_name": "Syhapod",
        "reply_to": 0,
        "text": "В полигон иди, тебе уже кидали",
        "level": 0,
        "time": 1675664948,
        "answers": []
      },
      {
        "id": 22485169,
        "author_name": "Котьмак из школы кота",
        "reply_to": 0,
        "text": "Дарю:",
        "level": 0,
        "time": 1675668258,
        "answers": []
      },
      {
        "id": 22485197,
        "author_name": "Котьмак из школы кота",
        "reply_to": 22485169,
        "text": "И в общей ленте не мусоришь, и за тем куда постишь следить не надо, и от лишних телодвижений по занесению тебя в чс окружающих избавляешь\nСплошные плюсы",
        "level": 1,
        "time": 1675668332,
        "answers": []
      },
      {
        "id": 23295777,
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
        "id": 22484013,
        "author_name": "Syhapod",
        "reply_to": 0,
        "text": "В полигон иди, тебе уже кидали",
        "level": 0,
        "time": 1675664948,
        "answers": []
      },
      {
        "id": 22485169,
        "author_name": "Котьмак из школы кота",
        "reply_to": 0,
        "text": "Дарю:",
        "level": 0,
        "time": 1675668258,
        "answers": []
      },
      {
        "id": 22485197,
        "author_name": "Котьмак из школы кота",
        "reply_to": 22485169,
        "text": "И в общей ленте не мусоришь, и за тем куда постишь следить не надо, и от лишних телодвижений по занесению тебя в чс окружающих избавляешь\nСплошные плюсы",
        "level": 1,
        "time": 1675668332,
        "answers": []
      },
      {
        "id": 23295777,
        "author_name": "Artem Glechinsky",
        "reply_to": 0,
        "text": "call of duty",
        "level": 0,
        "time": 1678118312,
        "answers": []
      }
    ]

set_a, set_b = set(a), set(b)
diff = set_a - set_b
print(diff)