#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 12:38:58 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError

from core.database.database_commands import retrieve_data_from_db
from core.database.database_engine import async_session_maker, engine
from core.database.database_models import CardBase

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class RemoveCard(StatesGroup):
    choose_card = State()
    remove_card = State()


@dp.message_handler(Text(equals='Remove card 🗑'))
@dp.message_handler(commands=['removecard'])
async def choose_card_for_removal(message: types.Message):
    items = select(CardBase).where(CardBase.user_id == str(message.from_user.id)) \
        .distinct(CardBase.my_set)

    items = await retrieve_data_from_db(items, async_session_maker)
    items = items.scalars().all()

    item_list = list()
    for item in items:
        item_list.append(item.my_set)

    sets = InlineKeyboardBuilder()

    for key in item_list:
        key = key.split(' ')
        key_text = '_'.join(key)
        key_callback = ('_'.join(key)).lower()
        key = InlineKeyboardButton(key_text, callback_data=key_callback)
        sets.add(key)

    await bot.send_message(message.from_id,
                           'A card from which set do you want to remove?',
                           reply_markup=sets)
