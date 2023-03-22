import aiohttp
import asyncio
import time

async def ddos(num = 10):
	for i in range(num):
		start = time.time()
		async with aiohttp.ClientSession() as session:
			async with session.get('http://127.0.0.1:8000/get_reply_to_my_comments', ssl=False) as resp:
				await resp.text()
				end = time.time() - start
				print(f"id_{i} in {end}'s done")

asyncio.run(ddos(100))