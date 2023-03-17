import asyncio
import random
import time


async def worker(name, queue):
    while True:
        # Получить "рабочий элемент" вне очереди.
        sleep_for = await queue.get()

        # Спать "sleep_for" секунд.
        await asyncio.sleep(sleep_for)

        # Сообщение очереди, для обработки "рабочего элемента".
        queue.task_done()

        print(f'{name} has slept for {sleep_for:.2f} seconds')


async def main():
    # Создать очередь, которую мы будем использовать для хранения нашей "рабочей нагрузки".
    queue = asyncio.Queue()

    # Генерирует случайные тайминги и помещает их в очередь.
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)

    # Создание трёх рабочих задач для одновременной обработки очереди.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # Подождать, пока очередь не будет полностью обработана.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Отменить рабочие задания.
    for task in tasks:
        task.cancel()
    # Подождать, пока все рабочие задачи не будут отменены.
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


asyncio.run(main())