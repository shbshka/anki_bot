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

from core.database.database_commands import query_to_db
from core.database.database_engine import async_session_maker
from core.database.database_models import CardBase


@dp.message(F.text=='My cards 📚')
@dp.message(Command('mycards'))
async def show_profile(message: types.Message):
    # query = select(CardBase) \
    #   .where(CardBase.user_id==str(message.from_user.id))
    # current_cards = await query_to_db(query, async_session_maker)
    # current_cards = current_cards.scalars().all()
    # cards = list()
    # for card in current_cards:
    #     cards.append(card.name)
    # cards = ', '.join(cards)

    # await bot.send_message(message.from_user.id,
    #                        '<b>✨YOUR CARDS✨</b>\n\n'
    #                        f'{cards}',
    #                        parse_mode='HTML')

    q = select(CardBase.my_set) \
        .where(CardBase.user_id == str(message.from_user.id)) \
            .distinct()
    my_sets = await query_to_db(q, async_session_maker)
    my_sets = my_sets.scalars().all()

    formatted = ''
    for my_set in my_sets:
        q = select(CardBase.name) \
            .where(CardBase.my_set == my_set)
        current_cards = await query_to_db(q, async_session_maker)
        current_cards = ', '.join(current_cards.scalars().all())
        formatted += f'set: {my_set}\ncards: {current_cards}\n\n'

    await bot.send_message(message.from_user.id,
                           '<b>Your cards:</b>\n\n'
                           f'{formatted}',
                           parse_mode='HTML')
