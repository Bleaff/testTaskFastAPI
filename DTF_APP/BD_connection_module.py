from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy import select
import sqlalchemy

import multibots_orm_models

bd_path = 'postgresql+asyncpg://multibot_user:fnlUd83jfK@188.225.14.56/multibots'# положи в .env
async_engine = create_async_engine(bd_path, pool_pre_ping=True)

class DataBaseConn:
    def __init__(self, bd_path)