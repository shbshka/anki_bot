#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:02:13 2023

@author: shbshka
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from core.database.database_engine import engine
from sqlalchemy.exc import SQLAlchemyError

async def add_item_to_db(item, my_async_session: AsyncSession):

    """ Adds an item to a database and rolls back if errors occured """

    async with my_async_session.begin() as session:
        try:
            session.add(item)
            return item
        except SQLAlchemyError as exc:
            print(exc)
            raise
        finally:
            await session.close()


async def retrieve_data_from_db(query, my_async_session: AsyncSession):

    """ Connects to the database and returns the results by a given query """

    async with my_async_session.begin() as session:
        try:
            executed_query = await session.execute(query)
        except SQLAlchemyError as exc:
            print(exc)
            raise
        finally:
            await session.close()
        return executed_query
