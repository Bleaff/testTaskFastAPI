import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from DTF import DTF
import asyncio

serv = FastAPI()


@serv.on_event("startup")
async def shedule_task_loop():
    serv.dtf = DTF(token = "79a24dbb2334b0a52a506db13f561cc006a6c2b52c12ed5ce2850eb5dd86a583")
    loop = asyncio.get_event_loop()
    loop.create_task(serv.dtf.get_all_my_entries())
    loop.create_task(serv.dtf.request_periodic_time())


@serv.get('/')
def root():
    html = """<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8">
  <title>Задача</title>
  <style type="text/css">
    .centered_line{
        display: flex;
        align-content: center;
        flex-direction: column;
    }
    p{
        width: 25%;
    }
   .line_left {
    display: flex;
    align-self: center;
    text-align: left;
    border-left: 2px solid rgb(0, 0, 0); /* Параметры линии */ 
    margin-left: 26%; /* Отступ слева */
    padding-left: 10px; /* Расстояние от линии до текста */
   }
   .line_right {
    display: flex;
    align-self: center;
    text-align: right;
    border-right: 2px solid rgb(0, 0, 0); /* Параметры линии */ 
    margin-right: 25%; /* Отступ слева */
    padding-right: 10px; /* Расстояние от линии до текста */ 
   }
  </style> 
 </head> 
 <body> 
    <center><h2>Написать класс DTF с интерфейсами для взаимодействия с сайтом https://dtf.ru.</h2></center>
    <div class="centered_line">
        <p class="line_left">Метод получения всех своих постов</p> 
        <p class="line_right">Метод получения комментариев к конкретному посту по его id</p> 
        <p class="line_left">Метод получения только новых комментариев к своим постам</p> 
        <p class="line_right">Метод получения ответов на свои комментарии с получением в ответе id родительского комментария</p> 
        <p class="line_left">Метод получения всей ветки комментария отдельного</p> 
        <p class="line_right">Сделать на это свое усмотрение, исходя из соображений, чтобы это было удобно использовать для автоматизации ответов на новые комментарии пользователей и посты. Чтобы удобно было потом получить только новые события, посмотреть в ответ на что они были сделаны эти события (просто комментарий к посту с указанием id родительского поста, возможно, сразу и текста родительского поста, или это комментарий к комментарию, или это ветка идет комментариев и т.п.). Чтобы удобно было сгенерировать новый ответ.</p>

            
    </div>

 </body>
    </html>"""
    return HTMLResponse(html)

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


@serv.get('/get_new_comments')
async def get_new_comments():
    """
        Метод получения новых комментариев со всех своих постов.
    """
    return await serv.dtf.get_new_comments()

@serv.get('/get_reply_to_my_comments')
async def get_reply():
    """
        Метод получения всех ответов на свои комментарии.
    """
    return await serv.dtf.get_answers_on_my_comments()

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

@serv.post("/add_entry_to_follow")
async def set_follow_entry(entry:int):
    return await serv.dtf.follow_entry(entry)