#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 12:38:58 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import delete

from core.database.database_commands import retrieve_data_from_db
from core.database.database_engine import async_session_maker, engine
from core.database.database_models import CardBase

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from core.universal_functions.functions import define_pagination


@dp.callback_query(lambda call: call.data == 'cancel')
async def cancel_removal(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id,
                           'Cancelled ✅')


@dp.message(F.text=='Remove card 🗑')
@dp.message(Command('removecard'))
async def choose_set_for_removal(message: types.Message, page=1):

    """ Shows the pages with sets """

    if type(message) == type(1):
        current_user_id = message
    else:
        current_user_id = message.from_user.id

    query = select(CardBase.my_set).where(CardBase.user_id == str(current_user_id)) \
        .distinct(CardBase.my_set)
    sets = await retrieve_data_from_db(query, async_session_maker)

    set_keyboard = await define_pagination(sets, page, 'set', '_')

    await bot.send_message(current_user_id,
                            'From which set do you want to remove a card?',
                            reply_markup=set_keyboard.as_markup())


@dp.callback_query(lambda call: call.data.startswith('set_to_'))
async def set_callback_handler(call: types.CallbackQuery):

    """ Flicks the pages with sets """

    page = int(call.data.split('_')[2])
    await call.message.delete()
    await choose_set_for_removal(call.from_user.id, page)


@dp.callback_query(lambda call: call.data.startswith('set_callback '))
async def choose_card_for_removal(call: types.CallbackQuery, page=1, callback=None):

    """ Shows the pages with cards """

    if type(call) == type('STRING'):
        my_set = call
    else:
        my_set = ' '.join(call.data.split(' ')[1::])

    q = select(CardBase.name).where(CardBase.my_set == my_set)
    cards = await retrieve_data_from_db(q, async_session_maker)

    card_keyboard = await define_pagination(cards, page, 'card', my_set)

    if callback == None:
        await bot.send_message(call.from_user.id,
                            'Which card do you want to remove?',
                            reply_markup=card_keyboard.as_markup())
    else:
        await bot.send_message(callback.from_user.id,
                            'Which card do you want to remove?',
                            reply_markup=card_keyboard.as_markup())


@dp.callback_query(lambda call: call.data.startswith('card_to_'))
async def card_callback_handler(call: types.CallbackQuery):

    """ Flicks the pages with cards """

    page = int(call.data.split('_')[2])
    call_data = call.data.split('_')[3]
    await call.message.delete()
    await choose_card_for_removal(call_data, page, call)


@dp.callback_query(lambda call: call.data.startswith('card_callback '))
async def card_removal(call: types.CallbackQuery):

    """ Removes the card from the database """

    card_name = ' '.join(call.data.split(' ')[1::])

    q = delete(CardBase).where(CardBase.name == card_name)
    await retrieve_data_from_db(q, async_session_maker)

    await bot.send_message(call.from_user.id, 'The card has been deleted! ✅')
