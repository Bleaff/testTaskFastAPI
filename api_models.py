from pydantic import BaseModel, parse_obj_as
import typing
from typing import List, Union
import datetime

class CommentTreeResponse(BaseModel):
    comment_id:int
    CommentTree:List[str]

class EntryResponse(BaseModel):
    entry_id : int
    CommentTrees: Union[List[CommentTreeResponse], None]

class GenerateCommentResponse(BaseModel):
    entries: List[EntryResponse]

class Response(BaseModel):
    comment_id:int
    Resp:str

class Entry_resp(BaseModel):
    entry_id: int
    CommentTrees: List[Response]

class GiveBackResponse(BaseModel):
    entries: Union[List[Entry_resp], None]


