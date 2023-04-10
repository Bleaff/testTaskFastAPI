import asyncio
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, text, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_session, create_async_engine, AsyncSession
from sqlalchemy import select

bd_path = 'postgresql+asyncpg://unlim:0000@127.0.0.1:5432/unlim_ad'

async_engine = create_async_engine(bd_path, pool_pre_ping=True, pool_size=30, max_overflow=30)





async def main():
    async with AsyncSession(async_engine) as async_session:
        try:           
            stmt = select(Bots.id, Bots.token, Pretexts.pretext).where(Bots.pretext_id == Pretexts.id)
            for item in await async_session.execute(stmt):
                print(item)
        except Exception as e:
            print(e)

asyncio.run(main())