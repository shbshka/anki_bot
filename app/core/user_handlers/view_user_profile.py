#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 00:05:24 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram import F
from aiogram.filters import Command

from sqlalchemy import select

from core.database.database_commands import retrieve_data_from_db
from core.database.database_engine import async_session_maker
from core.database.database_models import UserBase

import markups as nav


@dp.message(F.text=='My profile 🥷')
@dp.message(Command('myprofile'))
async def show_profile(message: types.Message):
    query = select(UserBase) \
        .where(UserBase.telegram_id==str(message.from_user.id))
    current_user = await retrieve_data_from_db(query, async_session_maker)
    current_user = current_user.scalar_one()
    await bot.send_message(message.from_user.id,
                           '<b>✨YOUR PROFILE✨</b>\n\n'
                           f'Username: <b>{current_user.username}</b>\n'
                           f'Name: <b>{current_user.name}</b>\n'
                           f'Surname: <b>{current_user.surname}</b>\n',
                           parse_mode='HTML',
                           reply_markup=nav.main_menu \
                               .as_markup(resize_keyboard=True))
