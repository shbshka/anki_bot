#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:02:13 2023

@author: shbshka
"""
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.exc import IntegrityError
from core.database.database_engine import engine, meta
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import select, insert

async def add_item_to_db(data, my_async_session: AsyncSession):

    """ Adds an item to a database and rolls back if errors occured """

    async with my_async_session.begin() as session:
        engine.execution_options(compiled_cache=None)
        try:
            session.add(data)
            await session.commit()
            return data
        except SQLAlchemyError as exc:
            print(exc)
            raise
        finally:
            await session.close()


async def retrieve_data_from_db(query, my_async_session):

    """ Connects to the database and returns the results by a given query """

    async with my_async_session.begin() as session:
        engine.execution_options(compiled_cache=None)
        try:
            executed_query = await session.execute(query)
            await session.commit()
        except SQLAlchemyError as exc:
            print(exc)
            raise
        finally:
            await session.close()
        return executed_query


# async def add_child_to_db(
#     query,
#     child,
#     my_async_session: AsyncSession):

#     """ Adds a child class to parent class """

#     async with my_async_session.begin() as session:
#         try:
#             parent = await session.execute(query)
#             parent = parent.first()
#             await parent.my_cards.append(child)
#         except SQLAlchemyError as exc:
#             print(exc)
#             raise
#         finally:
#             await session.close()
