import asyncio
from fastapi import FastAPI
from DTF_API import DTF
import asyncio

serv = FastAPI()

dtf = DTF(token = "79a24dbb2334b0a52a506db13f561cc006a6c2b52c12ed5ce2850eb5dd86a583")

@serv.on_event("startup")
async def shedule_task_loop():
    loop = asyncio.get_event_loop()
    loop.create_task(dtf.task_loop())

@serv.get('/')
def root():
    return "hello servers world"

@serv.get('/user/me/entries')
async def get_my_posts():
    """
        Метод получения всех своих постов по данному токену.
    """
    return await dtf.get_all_my_entries()

@serv.get("/entry/{id}/comments/popular")
async def get_comments_by_post_id(id:int):
    """
        Метод получения всех комментариев к посту по его id.
    """
    comment_tree = await dtf.get_comments_by_post_id(id)
    return await comment_tree.get_all_comments_as_dict()


@serv.get('/get_new_comments')
async def get_new_comments():
    """
        Метод получения новых комментариев со всех своих постов.
    """
    return await dtf.get_new_comments()

@serv.get('/get_reply_to_my_comments')
async def get_reply():
    """
        Метод получения всех ответов на свои комментарии.
    """
    return await dtf.get_answers_on_my_comments()

@serv.get('/get_comment_tree')
async def get_tree(comment_id):
    """
        Метод получения дерева комментариев для конкретного комментария.
    """
    return await dtf.get_comment_tree(comment_id)

@serv.post("/comment/add")
async def post_reply(entry_id:int, msg:str, id_to_reply:int = 0):
    return await dtf.reply_to_comment(entry_id, id_to_reply, msg)

@serv.get("/get_updates")
async def get_updates():
    return await dtf.get_updates()

@serv.get("/count")
async def get_updates_count():
    return await dtf.get_updates_count()