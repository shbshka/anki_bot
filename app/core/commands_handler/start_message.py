#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 06:04:17 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram.filters import Command
import markups as nav

from sqlalchemy import select

from core.database.database_commands import query_to_db
from core.database.database_models import UserBase
from core.database.database_engine import async_session_maker


@dp.message(Command('start'))
async def send_start_message(message: types.Message):

    """
    Checks the existence of the user in the database and shows
    the appropriate menu
    """

    telegram_id = str(message.from_user.id)
    query = select(UserBase).where(UserBase.telegram_id == telegram_id)
    result = await query_to_db(query, async_session_maker)
    result = result.first()

    if result != None:
        menu = nav.main_menu.as_markup(resize_keyboard=True)
    else:
        menu = nav.main_menu_anonymous.as_markup(resize_keyboard=True)

    await bot.send_message(message.from_user.id,
                           'Welcome to <b>ANKI Bot</b>! 🤓\n'
                           'This bot was designed to make your learning process'
                           ' easier and faster. 📈\n'
                           'To read the instructions, press /help',
                           parse_mode='HTML',
                           reply_markup=menu)
