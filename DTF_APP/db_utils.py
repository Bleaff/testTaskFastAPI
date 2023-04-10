import asyncio
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, text, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_session, create_async_engine, AsyncSession
from sqlalchemy import select

Base = declarative_base()
metadata = Base.metadata

bd_path = 'postgresql+asyncpg://unlim:0000@127.0.0.1:5432/unlim_ad' ########## TO CHANGE

async_engine = create_async_engine(bd_path, pool_pre_ping=True, pool_size=30, max_overflow=30)

class Pretexts(Base):
    __tablename__ = 'pretexts'
    id = Column(Integer, primary_key=True, unique=True)
    pretext = Column(String)

class Bots(Base):
    __tablename__ = 'bots'
    id = Column(Integer, primary_key=True, unique=True)
    dtf = Column(String)
    vc = Column(Boolean)
    pretext_id = Column(ForeignKey('pretexts.id'))

async def get_bots_credits(*bot_or_bots_id, column=Bots.dtf): #
    async with AsyncSession(async_engine) as async_session:
        try:           
            stmt = select(Bots.id, column, Pretexts.pretext).where(Bots.pretext_id == Pretexts.id).filter(Bots.id in bot_or_bots_id)
            response = await async_session.execute(stmt)
            if response is None:
                _error('Error with the query.')
                return None
            result = []
            for item in response:
                result.append({'id': item[0], 'token': item[1], 'pretext': item[2]})
            return result
        except Exception as e:
            print(e)