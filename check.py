import asyncio
from random import randint

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
