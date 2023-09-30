#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:49:38 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from core.database.database_engine import async_session_maker
from core.database.database_models import CardBase, UserBase
from core.database.database_commands import add_item_to_db, retrieve_data_from_db

from sqlalchemy import select

import markups as nav


class NewCard(StatesGroup):
    name = State()
    front = State()
    back = State()
    my_set = State()
    final = State()


@dp.message_handler(Text(equals='Cancel ⛔️'), state="*")
async def canced_card_adding(message: types.Message, state: FSMContext):

    """ Cancels the card adding """

    await bot.send_message(message.from_id,
                           'Adding a card has been cancelled 💔',
                           reply_markup=nav.card_menu)
    await state.finish()

@dp.message_handler(Text(equals='Add card 📝'), state='*')
async def send_invitation_message(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_id,
                           'Please write the name of your card',
                           reply_markup=nav.if_cancel)
    await state.set_state(NewCard.name)




@dp.message_handler(state=NewCard.name)
async def append_name(message: types.Message, state: FSMContext):

    """ Retrieves the name of the card """

    if len(message.text) > 1024:
        await bot.send_message(message.from_id,
                               'The name cannot be longer than <b>1024</b>'
                               ' characters.\n ✂️ Make the name shorter, please.'
                               ' You will add the front and the back to your'
                               ' card later.',
                               parse_mode='HTML')
    else:
        async with state.proxy() as data:
            data['card_name'] = message.text
        await bot.send_message(message.from_id,
                               'Please write the front of your card')
        await state.set_state(NewCard.front)


@dp.message_handler(state=NewCard.front)
async def append_front(message: types.Message, state: FSMContext):

    """ Retrieves the front of the card """

    if len(message.text) > 4000:
        await bot.send_message(message.from_id,
                               'The front cannot be longer than <b>4000</b>'
                               ' characters.\n ✂️ Make the front shorter,'
                               ' please.',
                               parse_mode='HTML')
    else:
        async with state.proxy() as data:
            data['front'] = message.text
        await bot.send_message(message.from_id,
                               'Please write the back of your card')
        await state.set_state(NewCard.back)


@dp.message_handler(state=NewCard.back)
async def append_back(message: types.Message, state: FSMContext):

    """ Retrieves the back of the card """

    if len(message.text) > 4000:
        await bot.send_message(message.from_id,
                               'The back cannot be longer than <b>4000</b>'
                               ' characters.\n ✂️ Make the back shorter,'
                               ' please.',
                               parse_mode='HTML')
    else:
        async with state.proxy() as data:
            data['back'] = message.text
        await bot.send_message(message.from_id,
                               'Now choose the set to which to add your card.')
    await state.set_state(state=NewCard.my_set)


@dp.message_handler(state=NewCard.my_set)
async def append_set(message: types.Message, state: FSMContext):

    """ Retrieves the set of the card """

    if len(message.text) > 4000:
        await bot.send_message(message.from_id,
                               'The set cannot be longer than <b>4000</b>'
                               ' characters.\n ✂️ Make the set shorter,'
                               ' please.',
                               parse_mode='HTML')
    else:
        async with state.proxy() as data:
            data['set'] = message.text
    await bot.send_message(message.from_id,
                           'Appending your card... 🕒')

    query = select(UserBase).where(UserBase.telegram_id==str(message.from_user.id))
    current_user = await retrieve_data_from_db(query, async_session_maker)
    current_user = current_user.scalar_one()
    print(f'\n\n\n\n{current_user}\n\n\n\n')
    async with state.proxy() as data:
        new_card = CardBase(
            name=data['card_name'],
            front=data['front'],
            back=data['back'],
            my_set=data['set'],
            user_id=current_user.telegram_id)
    await add_item_to_db(new_card, async_session_maker)
    await bot.send_message(message.from_id, 'The card has been appended! ✅')
    await state.finish()
