from fastapi import FastAPI
from DTF_API import DTF
from fastapi.responses import JSONResponse

serv = FastAPI()

dtf = DTF(token = "79a24dbb2334b0a52a506db13f561cc006a6c2b52c12ed5ce2850eb5dd86a583")

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
    return await dtf.get_comments_by_post_id(id)


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