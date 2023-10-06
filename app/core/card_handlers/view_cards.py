#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 04:37:50 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram import F
from aiogram.filters import Command

from sqlalchemy import select

from core.database.database_commands import retrieve_data_from_db
from core.database.database_engine import async_session_maker
from core.database.database_models import CardBase


@dp.message(F.text=='My cards 📚')
@dp.message(Command('mycards'))
async def show_profile(message: types.Message):
    query = select(CardBase).where(CardBase.user_id==str(message.from_user.id))
    current_cards = await retrieve_data_from_db(query, async_session_maker)
    current_cards = current_cards.scalars().all()
    cards = list()
    for card in current_cards:
        cards.append(card.name)

    await bot.send_message(message.from_user.id,
                           '<b>✨YOUR CARDS✨</b>\n\n'
                           f'{cards}',
                           parse_mode='HTML')
