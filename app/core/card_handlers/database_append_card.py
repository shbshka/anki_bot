#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:49:38 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from typing import Any, Dict

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


@dp.message(F.text=='Cancel card appending ⛔️')
async def canced_card_adding(message: types.Message, state: FSMContext):

    """ Cancels the card adding """

    await bot.send_message(message.from_user.id,
                           'Appending a card has been cancelled 💔',
                           reply_markup=nav.card_menu.as_markup(resize_keyboard=True))
    await state.clear()

@dp.message(F.text=='Add card 📝')
@dp.message(Command('addcard'))
async def send_invitation_message(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           'Please write the name of your card',
                           reply_markup=nav.if_cancel_card.as_markup(resize_keyboard=True))
    await state.set_state(NewCard.name)




@dp.message(NewCard.name)
async def append_name(message: types.Message, state: FSMContext):

    """ Retrieves the name of the card """

    if len(message.text) > 1024:
        await bot.send_message(message.from_user.id,
                               'The name cannot be longer than <b>1024</b>'
                               ' characters.\n ✂️ Make the name shorter, please.'
                               ' You will add the front and the back to your'
                               ' card later.',
                               parse_mode='HTML')
    else:
        await state.update_data(card_name=message.text)
        await bot.send_message(message.from_user.id,
                               'Please write the front of your card')
        await state.set_state(NewCard.front)


@dp.message(NewCard.front)
async def append_front(message: types.Message, state: FSMContext):

    """ Retrieves the front of the card """

    if len(message.text) > 4000:
        await bot.send_message(message.from_user.id,
                               'The front cannot be longer than <b>4000</b>'
                               ' characters.\n ✂️ Make the front shorter,'
                               ' please.',
                               parse_mode='HTML')
    else:
        await state.update_data(front=message.text)
        await bot.send_message(message.from_user.id,
                               'Please write the back of your card')
        await state.set_state(NewCard.back)


@dp.message(NewCard.back)
async def append_back(message: types.Message, state: FSMContext):

    """ Retrieves the back of the card """

    if len(message.text) > 4000:
        await bot.send_message(message.from_user.id,
                               'The back cannot be longer than <b>4000</b>'
                               ' characters.\n ✂️ Make the back shorter,'
                               ' please.',
                               parse_mode='HTML')
    else:
        await state.update_data(back=message.text)
        await bot.send_message(message.from_user.id,
                               'Now choose the set to which to add your card.')
    await state.set_state(state=NewCard.my_set)


@dp.message(NewCard.my_set)
async def append_set(message: types.Message, state: FSMContext):

    """ Retrieves the set of the card """

    if len(message.text) > 4000:
        await bot.send_message(message.from_user.id,
                               'The set cannot be longer than <b>4000</b>'
                               ' characters.\n ✂️ Make the set shorter,'
                               ' please.',
                               parse_mode='HTML')
    else:
        data = await state.update_data(my_set=message.text)
    await bot.send_message(message.from_user.id,
                           'Appending your card... 🕒')
    await state.clear()
    await append_to_db(message=message, data=data)

async def append_to_db(message: types.Message, data: Dict[str, Any], positive: bool = True) -> None:
    query = select(UserBase).where(UserBase.telegram_id==str(message.from_user.id))
    current_user = await retrieve_data_from_db(query, async_session_maker)
    current_user = current_user.scalar_one()
    new_card = CardBase(
        name = data['card_name'],
        front=data['front'],
        back=data['back'],
        my_set=data['my_set'],
        user_id=current_user.telegram_id)
    print(f'\n\n\n\n{new_card}\n\n\n\n')
    await add_item_to_db(new_card, async_session_maker)
    await bot.send_message(message.from_user.id,
                           'The card has been appended! ✅',
                           reply_markup=nav.card_menu)
