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

from core.universal_functions.functions import view_card_pagination

import markups as nav


@dp.message(F.text=='My cards 📚')
@dp.message(Command('mycards'))
async def show_sets(message: types.Message, page=1):

    if type(message) == type(1):
        current_user_id = message
    else:
        current_user_id = message.from_user.id

    q = select(CardBase.my_set) \
        .where(CardBase.user_id == str(message.from_user.id)) \
            .distinct()

    my_sets = await query_to_db(q, async_session_maker)

    view_cards_keyboard = await view_card_pagination(my_sets, page, 'view_set', '_')

    if view_cards_keyboard != 1:
        await bot.send_message(current_user_id,
                               'Choose the set to view cards:',
                               reply_markup=view_cards_keyboard.as_markup())
    else:
        await bot.send_message(current_user_id,
                               'You do not have any cards yet... 😞',
                               reply_markup=nav.card_menu \
                                   .as_markup(resize_keyboard=True))


@dp.callback_query(lambda call: call.data.startswith('set_to_'))
async def set_callback_handler(call: types.CallbackQuery):

    """ Flicks the pages with sets """

    page = int(call.data.split('_')[2])
    await call.message.delete()
    await show_sets(call.from_user.id, page)


@dp.callback_query(lambda call: call.data.startswith('view_set_callback '))
async def show_cards(call: types.CallbackQuery, page=1, callback=None):

    if type(call) == type('STRING'):
        my_set = call
    else:
        my_set = ' '.join(call.data.split(' ')[1::])

    q = select(CardBase.name).where(CardBase.my_set == my_set)
    cards = await query_to_db(q, async_session_maker)

    card_keyboard = await view_card_pagination(cards, page, 'view_card', my_set)

    if callback == None:
        await bot.send_message(call.from_user.id,
                            'Choose the card to view:',
                            reply_markup=card_keyboard.as_markup())
    else:
        await bot.send_message(callback.from_user.id,
                            'Choose the card to view:',
                            reply_markup=card_keyboard.as_markup())


@dp.callback_query(lambda call: call.data.startswith('card_to_'))
async def card_callback_handler(call: types.CallbackQuery):

    """ Flicks the pages with cards """

    page = int(call.data.split('_')[2])
    call_data = call.data.split('_')[3]
    await call.message.delete()
    await show_cards(call_data, page, call)


@dp.callback_query(lambda call: call.data.startswith('view_card_callback '))
async def show_content(call: types.CallbackQuery):

    card_name = ' '.join(call.data.split(' ')[1::])

    q = select(CardBase.front, CardBase.back, CardBase.tags) \
        .where(CardBase.name == card_name)
    card_info = await query_to_db(q, async_session_maker)
    card_info = card_info.first()

    await bot.send_message(call.from_user.id,
                           '<i>📖 Your card info:</i>\n\n'
                           f'<b>Card name:</b> {card_name}\n'
                           f'<b>Front:</b> {card_info[0]}\n'
                           f'<b>Back:</b> {card_info[1]}\n'
                           f'<b>Tags:</b> {card_info[2]}\n',
                           parse_mode='HTML')
