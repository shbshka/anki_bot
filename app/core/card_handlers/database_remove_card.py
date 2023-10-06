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

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class RemoveCard(StatesGroup):
    choose_card = State()
    remove_card = State()


@dp.message(F.text=='Remove card 🗑')
@dp.message(Command('removecard'))
async def choose_set_for_removal(message: types.Message, page=1):


    #============INFO RETRIEVING=========

    if type(message) == type(1):
        current_user_id = message
    else:
        current_user_id = message.from_user.id

    q_set = select(CardBase).where(CardBase.user_id == str(current_user_id)) \
        .distinct(CardBase.my_set)
    sets = await retrieve_data_from_db(q_set, async_session_maker)
    set_items = sets.scalars().all()
    set_count = len(set_items)

    set_list = list()
    for item in set_items:
        set_list.append(item.my_set)


    #===============SWITCHERS============

    left = page - 1 if page != 1 else set_count
    right = page + 1 if page != set_count else 1


    #==========CORE OF THE KEYBOARD=======

    left_button = InlineKeyboardButton(text='⬅️back', callback_data=f'to_{left}')
    right_button = InlineKeyboardButton(text='forward➡️', callback_data=f'to_{right}')
    display_buttons = []


    #===CHANGEABLE PART OF THE KEYBOARD===

    for set_name in set_list:
        set_callback = 'set_callback_' + '_'.join(set_name.split(' '))
        set_button = InlineKeyboardButton(text=f'{set_name}',
                                          callback_data=f'{set_callback}')
        display_buttons.append(set_button)

    #========BUILDING A KEYBOARD=========

    sets = InlineKeyboardBuilder()

    def button_splitter(buttons, n):
        for i in range(0, len(buttons), n):
            yield buttons[i: i + n]

    button_sets = list(button_splitter(display_buttons, 8))


    page_button = InlineKeyboardButton(text=f'{str(page)}/{str(len(button_sets))}',
                                       callback_data='_')

    sets.add(
        left_button,
        page_button,
        right_button
        )

    buttons = button_sets[page - 1]
    for button in buttons:
        sets.add(button)

    sets.adjust(3, 4)


    await bot.send_message(current_user_id,
                            'From which set do you want to remove a card?',
                            reply_markup=sets.as_markup())


@dp.callback_query(lambda call: call.data.startswith('to_'))
async def set_callback_handler(call: CallbackData):
    page = int(call.data.split('_')[1])
    await call.message.delete()
    await choose_set_for_removal(call.from_user.id, page=page)


@dp.callback_query(lambda call: call.data.startswith('set_callback_'))
async def choose_card_for_removal(call, page=1):

    #============INFO RETRIEVING=========

    my_set = (' ').join(call.data.split('_')[2::])

    q = select(CardBase.name).where(CardBase.my_set == my_set)
    cards_query = await retrieve_data_from_db(q, async_session_maker)
    my_cards = cards_query.scalars().all()
    cards_length = len(my_cards)

    card_list = list()
    for card in my_cards:
        card_list.append(card)


    #===============SWITCHERS============

    left = page - 1 if page != 1 else cards_length
    right = page + 1 if page != cards_length else 1

    #==========CORE OF THE KEYBOARD=======

    left_button = InlineKeyboardButton(text='⬅️back', callback_data=f'card_to_{left}')
    right_button = InlineKeyboardButton(text='forward➡️', callback_data=f'card_to_{right}')
    display_buttons = []

    #===CHANGEABLE PART OF THE KEYBOARD===

    for card_name in card_list:
        card_callback = 'card_callback_' + '_'.join(card_name.split(' '))
        card_button = InlineKeyboardButton(text=f'{card_name}',
                                          callback_data=f'{card_callback}')
        display_buttons.append(card_button)


    #========BUILDING A KEYBOARD=========

    cards = InlineKeyboardBuilder()

    def button_splitter(buttons, n):
        for i in range(0, len(buttons), n):
            yield buttons[i: i + n]

    button_cards = list(button_splitter(display_buttons, 8))
    page_button = InlineKeyboardButton(text=f'{str(page)}/{str(len(button_cards))}',
                                       callback_data='_')

    cards.add(
        left_button,
        page_button,
        right_button
        )

    buttons = button_cards[page - 1]
    for button in buttons:
        cards.add(button)

    cards.adjust(3, 4)

    await bot.send_message(call.from_user.id,
                            'Which card do you want to remove?',
                            reply_markup=cards.as_markup())


@dp.callback_query(lambda call: call.data.startswith('card_to_'))
async def card_callback_handler(call: CallbackData):
    page = int(call.data.split('_')[2])
    await call.message.delete()
    await choose_card_for_removal(call, page=page)


@dp.callback_query(lambda call: call.data.startswith('card_callback_'))
async def card_removal(call):
    card_name = call.data.split('_')[2]

    print(card_name)

    q = delete(CardBase).where(CardBase.name == card_name)
    await retrieve_data_from_db(q, async_session_maker)

    await bot.send_message(call.from_user.id, 'The card has been deleted! ✅')
