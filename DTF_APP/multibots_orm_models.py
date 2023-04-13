# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('accounts_id_seq'::regclass)"))
    dtf = Column(String)


class Advertising(Base):
    __tablename__ = 'advertising'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('advertising_id_seq'::regclass)"))
    name = Column(String)
    description = Column(String)
    balance = Column(Integer, server_default=text("0"))


class Instruction(Base):
    __tablename__ = 'instructions'

    id = Column(Integer, primary_key=True, unique=True)
    text = Column(String)


class Bot(Base):
    __tablename__ = 'bots'

    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('bots_id_seq'::regclass)"))
    id_account = Column(ForeignKey('accounts.id'))
    id_instruction = Column(ForeignKey('instructions.id'))
    id_advertising = Column(ForeignKey('advertising.id'))
    active = Column(Boolean, server_default=text("false"))
    memory = Column(String)

    account = relationship('Account')
    advertising = relationship('Advertising')
    instruction = relationship('Instruction')
