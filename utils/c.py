import asyncpg
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy import Column
from sqlalchemy import String

meta = MetaData()

t1 = Table("bots", meta, Column("id", String(50), primary_key=True))


async def main():
    db_engine = await asyncpg.connect(user='unlim', database='unlim_ad', host='127.0.0.1', password='0000')
    result = []
    res = await db_engine.fetch("""select * from bots""")
    result = [dict(row) for row in res]
    print(result)

asyncio.run(main())