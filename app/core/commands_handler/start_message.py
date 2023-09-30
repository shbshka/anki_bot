#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 06:04:17 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
import markups as nav

from sqlalchemy import select


from core.database.database_commands import retrieve_data_from_db
from core.database.database_models import UserBase
from core.database.database_engine import async_session_maker, engine


@dp.message_handler(commands=['start'])
async def send_start_message(message: types.Message):

    """
    Checks the existence of the user in the database and shows
    the appropriate menu
    """

    telegram_id = str(message.from_user.id)
    query = select(UserBase).where(UserBase.telegram_id == telegram_id)
    result = await retrieve_data_from_db(query, engine)
    result = result.first()

    if result != None:
        menu = nav.main_menu
    else:
        menu = nav.main_menu_anonymous

    await bot.send_message(message.from_id,
                           'Welcome to <b>ANKI Bot</b>! 🤓\n'
                           'This bot was designed to make your learning process'
                           ' easier and faster. 📈\n'
                           'To read the instructions, press /help',
                           parse_mode='HTML',
                           reply_markup=menu)
