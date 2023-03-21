import asyncio

class a:
	def __init__(self, a):
		self.a = a
		self.res = self.check()

	async def slp(self):
		await asyncio.sleep(.3)
		return {"Gut"}

	def run_in_init(func):
		async def wrapper(func):
			return await func()
		return await wrapper

	@run_in_init
	async def check(self):
		return await self.slp()


ob = a("fsc")
print(ob.a)