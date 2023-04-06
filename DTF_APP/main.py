##!/bin/bash
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from OsnovaApiConnect import OsnovaApiConn
import asyncio
import uvicorn
from signalization import _info
from Comment import CommentTree
from BotTracker import BotTracker
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:5241@localhost:5432/unlim_ad")
serv = FastAPI()

t1 = '555ea53407c0b2455a6479fec5b3893ebf3fa674bffdebb5327e878696bfe263'
t2 = "79a24dbb2334b0a52a506db13f561cc006a6c2b52c12ed5ce2850eb5dd86a583"

bd = 'unlim_ad'

@serv.on_event("startup")
async def shedule_task_loop():
    serv.task_tracker = BotTracker(OsnovaApiConn(t1), OsnovaApiConn(t2))
    for bot in serv.task_tracker.bots_pool:
        await bot.run_setup()
    await serv.task_tracker.active_pool_bots()
    _info('    Startup complete!')

@serv.get('/user/me/entries')
async def get_my_posts():
    """
        Метод получения всех своих постов по данному токену.
    """
    return await serv.dtf.get_all_my_entries()

@serv.get("/entry/{id}/comments/popular")
async def get_comments_by_post_id(id:int):
    """
        Метод получения всех комментариев к посту по его id.
    """
    comment_tree = await serv.dtf.get_comments_by_post_id(id)
    return comment_tree.get_all_comments_as_dict()

@serv.get('/get_comment_tree')
async def get_tree(comment_id):
    """
        Метод получения дерева комментариев для конкретного комментария.
    """
    return await serv.dtf.get_comment_tree(comment_id)

@serv.post("/comment/add")
async def post_reply(entry_id:int, msg:str, id_to_reply:int = 0):
    return await serv.dtf.reply_to_comment(entry_id, id_to_reply, msg)

@serv.get("/get_updates")
async def get_updates():
    return await serv.dtf.get_updates()

@serv.get("/count")
async def get_updates_count():
    return await serv.dtf.get_updates_count()

@serv.get('/get_followed_entries')
async def get_entries():
    """Метод получения записей, отслеживаемые ботом """
    return serv.dtf.get_followed_entries()

@serv.post("/add_entry_to_follow/{entry}")
async def set_follow_entry(entry:int):
    return await serv.dtf.follow_entry(entry)

if __name__ == "__main__":
    uvicorn.run("main:serv", port=38000, reload=True)