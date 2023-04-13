import asyncio
from fastapi import FastAPI
from OsnovaApiConnect import OsnovaApiConn
import uvicorn
from signalization import _info
from BotTracker import BotTracker
from api_models import *
from multibots_orm_models import Account, Advertising, Instruction, Bot 

serv = FastAPI()

@serv.on_event("startup")
async def shedule_task_loop():




@serv.get("/get_entry/{entry_id}")
async def get_entry(entry_id:int, bot_token:str, pretext:str):
    bot = OsnovaApiConn(token=bot_token, pretext=pretext, bd_id=0, place='dtf')
    entry = await bot.get_full_entry(entry_id)
    return entry

@serv.post('/listen_entry/{entry_id}')
async def set_to_listen(entry_id:int, bot_id:int): #добавим
    """
        Ответ ботом на комментарии записи по id. Ответ на n% от всех комментариев, далее лишь прослушивание ответов в базовом режиме.
    """
    try:
        choosen_bot = serv.task_tracker.get_bot_by_id(bot_id)
        if not choosen_bot:
            return "Bot doesn't exist!"
        await choosen_bot.enterance_into_foreign_entry(entry_id)
    except Exception as e:
        _error(e)
        return e

@serv.get('/get_active_bots')
async def get_active():
	try:
		if serv.task_tracker is None:
			return "Bots haven't been set up"
		return serv.task_tracker.get_active_bot()
	except Exception as e:
		_error(e)
		return e

@serv.get('/get_comment_tree_for_comment/{comment_id}')
async def get_ct(entry_id:int, comment_id:int, bot_token:str):
    bot = OsnovaApiConn(token=bot_token, pretext='', bd_id='', place='dtf')
    entry = await bot.get_full_entry(entry_id)
    return await entry.comments.make_comment_tree_v2(comment_id)

@serv.get('/get_max_tree/{entry_id}')
async def get_mt(entry_id:int, bot_token:str):
    bot = OsnovaApiConn(token=bot_token, pretext='', bd_id='', place='dtf')
    entry = await bot.get_full_entry(entry_id)
    all_comments = entry.comments.get_all_comments()
    all_trees = await asyncio.gather(*[entry.comments.make_comment_tree_v2(comment.id) for comment in all_comments])
    max_len = all_trees[0]
    for tree in all_trees:
        if len(tree) > len(max_len):
            max_len = tree
    return max_len

if __name__ == "__main__":
    uvicorn.run("main:serv", port=38000, reload=True)