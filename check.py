import asyncio
<<<<<<< HEAD
from random import randint
=======
from DTF_API import DTF
dtf = DTF(token = "79a24dbb2334b0a52a506db13f561cc006a6c2b52c12ed5ce2850eb5dd86a583")
async def posts():
    # posts = await dtf.get_comments_by_post_id(1679156)
    # print(posts.get_all_comments_as_dict()) #есть метод str, который приводит к виду диалога, если нужен вид словаря. то необходима такая запись
    tree = await dtf.get_comment_tree(23373325)
    print(posts)
asyncio.run(posts())
>>>>>>> 2937ddb3589ceffba24b0e84dee4aeae8d637ea9

async def timer(delay):
    await asyncio.sleep(delay)
    print(f"Delay {delay}s done")
    return {"result": {
        "gad": 1,
        "bless": 2
    }}

async def run_tasks(tasks):
    for task in tasks:
        await task

# async def main():
#     for i in range(5, 100, 5):
#         tasks = [asyncio.create_task(timer(i)) for i in range(5, 100, 5)]
#     await run_tasks(tasks)
async def main():
    # complited = await asyncio.gather(*[asyncio.create_task(timer(i)) for i in range(5, 25, 5)])
    while True:
        rand_time = randint(3, 10)
        res = await timer(rand_time)
        print(res)

asyncio.run(main())
# loop = asyncio.get_event_loop()
# loop.create_task(main())
# loop.run()

#Асинхрон получен! 
"""
    Идея асинхронных запросов к серверу в рандомное время: 
        Асинхронная функция принимает на вход число delay - время до следующей отправки запросов и список сформированных задач...
"""
