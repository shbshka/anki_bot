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

from core.database.database_engine import engine, async_session_maker
from core.database.database_models import CardBase
from core.database.database_commands import add_item_to_db

import markups as nav


class NewCard(StatesGroup):
    name = State()
    front = State()
    back = State()


@dp.message_handler(Text(equals='Cards 🃏'))
@dp.message_handler(commands=['cards'])
async def cards_menu(message: types.Message):
    await bot.send_message(message.from_id,
                           'Here are your cards, Learner! 🤓',
                           reply_markup=nav.card_menu)


@dp.message_handler(Text(equals='Add card 📝'), state='*')
async def send_invitation_message(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_id,
                           'Please write the name of your card')
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
            data['name'] = message.text
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
                               'Appending your card... 🕒')
        await state.finish()


async def append_all(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        new_card = CardBase(
            name=data['name'],
            front=data['front'],
            back=data['back'],
            user_id=str(message.from_user.id)
            )
    await add_item_to_db(item=new_card, my_async_session=async_session_maker)
    await bot.send_message(message.from_id, 'The card has been appended! ✅')
