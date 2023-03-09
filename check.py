import asyncio
from DTF_API import DTF
dtf = DTF(token = "79a24dbb2334b0a52a506db13f561cc006a6c2b52c12ed5ce2850eb5dd86a583")
async def posts():
    # posts = await dtf.get_comments_by_post_id(1679156)
    # print(posts.get_all_comments_as_dict()) #есть метод str, который приводит к виду диалога, если нужен вид словаря. то необходима такая запись
    tree = await dtf.get_comment_tree(23373325)
    print(posts)
asyncio.run(posts())

