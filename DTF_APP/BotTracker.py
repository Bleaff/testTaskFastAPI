from OsnovaApiConnect import OsnovaApiConn
import asyncio

class BotTracker:
	def __init__(self, *bot_or_bots):
		self.bots_pool = []
		for bot in bot_or_bots:
			self.bots_pool.append(bot)

	async def add_to_pool(self, *bot_or_bots):
		"""Добавление ботов в качестве прослушивающих своих записей (добавленных в entries в самих ботах)."""
		for bot in bot_or_bots:
			await bot.run_setup()
			self.bots_pool.append(bot)

	async def active_pool_bots(self):
		#Set active (runs endless cycle for each bot whith non-active property)
		for bot in self.bots_pool:
			await bot.start_my_task()
	
	async def cancel_task(self, *bot_or_bots_name):
		for name in bot_or_bots_name:
			for bot in self.bots_pool:
				if name == bot.user_info.name:
					bot.cancel_my_task()
	
	async def stop_all_bots(self):
		for bot in self.bots_pool:
			bot.cancel_task()