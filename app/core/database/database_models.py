#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:33:58 2023

@author: shbshka
"""
import asyncio
from sqlalchemy import ForeignKey, MetaData, inspect, Table
from sqlalchemy.orm import (declarative_base,
                            relationship,
                            Mapped,
                            mapped_column,
                            backref,
                            )
import sqlalchemy.types as types

from core.database.database_engine import engine
from sqlalchemy import (Column,
                        Integer,
                        String,
                        Text,
                        Enum)

from typing import List, Optional

import enum


Base = declarative_base()
metadata = MetaData()


class LearnStatusEnum(enum.Enum):
    bad = 0
    medium = 1
    good = 2
    excellent = 3


class UserBase(Base):

    """ An account for storing and accessing multiple learning cards """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String, unique=True)
    username = Column(String(100), unique=True)
    name = Column(String(200))
    surname = Column(String(200))
    my_cards: Mapped[Optional['CardBase']] = relationship(back_populates='my_user')


class CardBase(Base):

    """ A learning card with front and back text bound to a specific user """

    __tablename__ = 'cards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.telegram_id'))
    my_user: Mapped['UserBase'] = relationship(back_populates='my_cards')
    name = mapped_column(Text)
    front = mapped_column(Text)
    back = mapped_column(Text)
    my_set = mapped_column(Text)
    tags = mapped_column(Text, default='')
    learn_status = mapped_column('learn_status', Enum(LearnStatusEnum),
                                 default=LearnStatusEnum.bad)


async def init_models():

    """ Creates the above-mentioned tables """

    async with engine.begin() as conn:
        try:
            await conn.run_sync(UserBase.metadata.create_all)
            await conn.run_sync(CardBase.metadata.create_all)
            await conn.commit()
        finally:
            await conn.close()


async def get_users():

    """ Retrieves all information from Users """

    async with engine.begin() as conn:
        users_table = Table('users', metadata)
        users = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).reflect_table(
                users_table, None
                )
            )
        await conn.commit()
        await conn.close()
        return users


async def get_cards():

    """ Retrieves all information from Cards """

    async with engine.begin() as conn:
        cards_table = Table('cards', metadata)
        cards = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).reflect_table(
                cards_table, None
                )
            )
        await conn.commit()
        await conn.close()
        return cards
