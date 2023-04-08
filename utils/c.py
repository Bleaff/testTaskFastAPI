import asyncio
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, text, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_session, create_async_engine, AsyncSession
from sqlalchemy import select

bd_path = 'postgresql+asyncpg://unlim:0000@127.0.0.1:5432/unlim_ad'

async_engine = create_async_engine(bd_path, pool_pre_ping=True, pool_size=30, max_overflow=30)

Base = declarative_base()
metadata = Base.metadata


class Pretexts(Base):
    __tablename__ = 'pretexts'
    id = Column(Integer, primary_key=True, unique=True)
    pretext = Column(String)

class Bots(Base):
    __tablename__ = 'bots'
    id = Column(Integer, primary_key=True, unique=True)
    token = Column(String)
    place = Column(Boolean)
    pretext_id = Column(ForeignKey('pretexts.id'))



async def main():
    async with AsyncSession(async_engine) as async_session:
        try:           
            stmt = select(Bots).where(Bots.place == 'dtf')
            items = await async_session.execute(stmt)
            qresult = items.all()
            for item in qresult:
                print(item[0])
        except Exception as e:
            print(e)

asyncio.run(main())