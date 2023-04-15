from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy import select
import sqlalchemy
import multibots_orm_models
import os
from dotenv import load_dotenv, find_dotenv
from signalization import _error


class DataBaseConn:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.async_engine = create_async_engine(os.environ.get("BD_CON_STRING"), pool_pre_ping=True)

    async def get_full_info_bots(self, ids:list[int])->list[dict]:
        async with AsyncSession(self.async_engine) as async_session:
            stmt = select(multibots_orm_models.Bot.id, 
                          multibots_orm_models.Bot.active,
                          multibots_orm_models.Bot.memory,
              multibots_orm_models.Instruction.id,
              multibots_orm_models.Instruction.text,
              multibots_orm_models.Advertising.id,
              multibots_orm_models.Advertising.name,
              multibots_orm_models.Advertising.balance,
              multibots_orm_models.Account.id,
              multibots_orm_models.Account.dtf).where(multibots_orm_models.Bot.id.in_(ids))\
              .join(multibots_orm_models.Account, multibots_orm_models.Bot.id_account == multibots_orm_models.Account.id)\
              .join(multibots_orm_models.Advertising, multibots_orm_models.Bot.id_advertising == multibots_orm_models.Advertising.id)\
              .join(multibots_orm_models.Instruction, multibots_orm_models.Bot.id_instruction == multibots_orm_models.Instruction.id)
            items = await async_session.execute(stmt)
            items = items.all()
            ress = []
            for item in items:
                bot = {'id': item[0], 'active': item[1], 'memory': item[2], 'instruction_id': item[3], 'instruction_text': item[4], 
                       'advertising_id': item[5], 'advertising_name': item[6], 'advertising_balance': item[7], 
                       'account_id': item[8], 'account_dtf': item[9]}
                ress.append(bot)
            return ress
    
    async def decrement_advertising_balance(self, id_advertising:int, tokens_used:int):
        async with AsyncSession(self.async_engine) as async_session:
            stmt = select(multibots_orm_models.Advertising).where(multibots_orm_models.Advertising.id == id_advertising)
            items = await async_session.execute(stmt)
            item = items.scalars().first()
            item.balance -= tokens_used
            async_session.add(item)
            await async_session.commit()

    async def get_all_active(self):
        async with AsyncSession(self.async_engine) as async_session:
            stmt = select(multibots_orm_models.Bot.id, 
                          multibots_orm_models.Bot.active,
                          multibots_orm_models.Bot.memory,
              multibots_orm_models.Instruction.id,
              multibots_orm_models.Instruction.text,
              multibots_orm_models.Advertising.id,
              multibots_orm_models.Advertising.name,
              multibots_orm_models.Advertising.balance,
              multibots_orm_models.Account.id,
              multibots_orm_models.Account.dtf).where(multibots_orm_models.Bot.active == True)\
              .join(multibots_orm_models.Account, multibots_orm_models.Bot.id_account == multibots_orm_models.Account.id)\
              .join(multibots_orm_models.Advertising, multibots_orm_models.Bot.id_advertising == multibots_orm_models.Advertising.id)\
              .join(multibots_orm_models.Instruction, multibots_orm_models.Bot.id_instruction == multibots_orm_models.Instruction.id)
            items = await async_session.execute(stmt)
            items = items.all()
            ress = []
            for item in items:
                bot = {'id': item[0], 'active': item[1], 'memory': item[2], 'instruction_id': item[3], 'instruction_text': item[4], 
                       'advertising_id': item[5], 'advertising_name': item[6], 'advertising_balance': item[7], 
                       'account_id': item[8], 'account_dtf': item[9]}
                ress.append(bot)
            return ress

    async def get_rest_token(self, id_advertising:int)->int:
        async with AsyncSession(self.async_engine) as async_session:
            stmt = select(multibots_orm_models.Advertising).where(multibots_orm_models.Advertising.id == id_advertising)
            items = await async_session.execute(stmt)
            try :
                item = items.scalars().first()
                return item.balance
            except AttributeError as ae:
                _error("Missing the statement in db")
                return 0
            except Exception as e:
                _error("Missing the statement in db")

        