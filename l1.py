import asyncio
async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

async def main():
    # Запланировать дерево вызовов *конкурентно*:
    coro_list = [factorial("A", 2),factorial("B", 3),factorial("C", 4), factorial("D", 4), factorial("E", 5)]
    tasks = [asyncio.create_task(coro) for coro in coro_list] 
    while True:
        await asyncio.gather(*tasks)
        tasks = [asyncio.create_task(coro) for coro in coro_list] 

asyncio.run(main())