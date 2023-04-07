import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from OsnovaApiConnect import OsnovaApiConn
import asyncio
import uvicorn
from signalization import _info
from Comment import CommentTree
from BotTracker import BotTracker
import asyncpg

serv = FastAPI()

@serv.on_event("startup")
async def shedule_task_loop():
    serv.db_engine = await asyncpg.connect(user='unlim', database='unlim_ad', host='127.0.0.1', password='0000') #Здесь стоит поменять подключение к дб
    res = await serv.db_engine.fetch("""
                                        SELECT bots.id, bots.token, bots.place, pretexts.pretext FROM bots
                                        LEFT JOIN pretexts on bots.pretext_id=pretexts.id
                                    """)
    bot_credits_list = [dict(row) for row in res]
    _info(bot_credits_list)
    bots = [OsnovaApiConn(credit['token'], pretext=credit['pretext'], bd_id=credit['id'], place=credit['place']) for credit in bot_credits_list]
    serv.task_tracker = BotTracker(*bots)
    for bot in serv.task_tracker.bots_pool:
        await bot.run_setup()
    await serv.task_tracker.active_pool_bots()
    _info('   Startup complete!')

@serv.get("/get_entry/{entry_id}")
async def get_entry(entry_id:int):
    bot = OsnovaApiConn(t1)
    entry = await bot.get_full_entry(entry_id)
    return entry

@serv.post('/listen_entry/{entry_id}')
async def set_to_listen(entry_id:int, bot_id:int): #добавим
    """
        Ответ ботом на комментарии записи по id. Ответ на n% от всех комментариев, далее лишь прослушивание ответов в базовом режиме.
    """
    choosen_bot = serv.task_tracker.get_bot_by_id(bot_id)
    if not choosen_bot:
        return "Bot doesn't exist!"
    await choosen_bot.enterance_into_foreign_entry(entry_id)

@serv.get('/get_bots_db_values')
async def get_bots_info():
    res = await serv.db_engine.fetch("""
                                        SELECT bots.id, bots.token, bots.place, pretexts.pretext FROM bots
                                        LEFT JOIN pretexts on bots.pretext_id=pretexts.id
                                    """)
    return [dict(row) for row in res]

@serv.get('/get_active_bots')
async def get_active():
    return serv.task_tracker.get_active_bot()

if __name__ == "__main__":
    uvicorn.run("main:serv", port=38000, reload=True)