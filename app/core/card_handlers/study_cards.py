#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 16:29:25 2023

@author: shbshka
"""
from loader import bot, dp

from aiogram import types
from aiogram import F
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from sqlalchemy import select, update

import markups as nav
from core.database.database_models import CardBase, LearnStatusEnum
from core.universal_functions.functions import define_pagination
from core.database.database_commands import query_to_db
from core.database.database_engine import async_session_maker

import random


class Study(StatesGroup):
    initial = State()
    front = State()
    back = State()


@dp.message(F.text == 'Cancel studying ⛔️')
async def cancel_studying(message: types.Message, state: FSMContext):

    """ Cancels studying """

    await bot.send_message(message.from_user.id,
                           'Studying cancelled 💔',
                           reply_markup=nav.card_menu \
                               .as_markup(resize_keyboard=True))
    await state.clear()


@dp.callback_query(lambda call: call.data == 'cancel_study')
async def finish_studying(call: types.CallbackQuery, state: FSMContext):

    """ Completes studying """

    await bot.send_message(call.from_user.id,
                           'Studying cancelled 💔',
                           reply_markup=nav.card_menu \
                               .as_markup(resize_keyboard=True))
    await state.clear()


@dp.message(F.text=='Study 😵‍💫')
@dp.message(Command('study'))
async def select_set(message: types.Message, state: FSMContext, page=1):

    """ Selects the set that is required to be studied """

    query = select(CardBase.my_set) \
        .where(CardBase.user_id == str(message.from_user.id)).distinct()
    items = await query_to_db(query, async_session_maker)

    study_keyboard = await define_pagination(items, page, 'study', None)

    if study_keyboard != -1:
        await bot.send_message(message.from_user.id,
                               'Choose the set to study',
                               reply_markup=study_keyboard \
                                   .as_markup(resize_keyboard=True))
        await state.set_state(Study.front)
    else:
        await bot.send_message(message.from_user.id,
                               'You do not have any cards yet... 😞',
                               reply_markup=nav.card_menu \
                                   .as_markup(resize_keyboard=True))


@dp.callback_query(lambda call: call.data.startswith('set_to_'))
async def set_callback_handler(call: types.CallbackQuery):

    """ Flicks the pages with sets """

    page = int(call.data.split('_')[2])
    await call.message.delete()
    await select_set(call.from_user.id, page)


@dp.callback_query(lambda call: call.data.startswith('study_callback'))
async def determine_set(call: types.callback_query, state: FSMContext):

    """ Initial studying state """

    set_name = ' '.join(call.data.split(' ')[1::])

    await bot.send_message(call.from_user.id,
                           f'You are studying set {set_name}.\n'
                           'press \'Continue studying 📚\' to continue, '
                           'press \'Cancel studying ⛔️\' to stop.',
                           reply_markup=nav.if_cancel_study.as_markup())
    await state.update_data(initial=set_name)

    await state.set_state(Study.front)


@dp.message(F.text == 'Continue studying 📚')
async def study_card_front(message: types.Message, card_num=0):

    """ Sending card front """

    state = dp.fsm.resolve_context(bot=bot, chat_id=message.chat.id,
                                   user_id=message.from_user.id)

    set_name = await state.get_data()
    set_name = ''.join([x for x in set_name.values()][0])

    q = select(CardBase.front).where(CardBase.my_set == set_name)
    my_set_fronts = await query_to_db(q, async_session_maker)
    my_set_fronts = my_set_fronts.scalars().all()

    card_front = my_set_fronts[card_num]

    await state.update_data(card_front=card_front)

    await bot.send_message(message.from_user.id,
                           f'Card front: {card_front}.\n'
                           'Now type the answer!',) #add stop markup
    await state.set_state(Study.back)


@dp.message(Study.back)
async def study_card_back(message: types.Message, state: FSMContext):

    """ Asserts equal back and selects the next card """

    card_fronts = await state.get_data()
    card_front = ''.join([x for x in card_fronts.values()][1])

    q = select(CardBase.back).where(CardBase.front == card_front)
    back = await query_to_db(q, async_session_maker)
    back = ''.join(back.scalars().all())

    my_set = await state.get_data()
    my_set = [x for x in my_set.values()]
    my_set = my_set[1]

    q = select(CardBase.front).where(CardBase.my_set == my_set)
    my_set_fronts = await query_to_db(q, async_session_maker)
    my_set_fronts = my_set_fronts.scalars().all()

    try:
        card_num = random.randint(0, len(my_set_fronts) - 1)
    except ValueError:
        card_num = 0 #can insert studying completed here

    input_back = message.text
    if back == input_back:
        await bot.send_message(message.from_user.id,
                               'Correct ✅')

        q = select(CardBase.learn_status) \
            .where(CardBase.back == back)
        old_learn_status = await query_to_db(q, async_session_maker)
        old_learn_status = old_learn_status.scalars().all()[0].value

        if old_learn_status != 3:
            new_learn_status = old_learn_status + 1

        status_enum = LearnStatusEnum(new_learn_status)

        q = update(CardBase) \
            .values(learn_status=status_enum) \
                .where(CardBase.user_id == str(message.from_user.id))
        await query_to_db(q, async_session_maker)

        await study_card_front(message=message,
                               card_num=card_num)
    else:
        await bot.send_message(message.from_user.id,
                               'Incorrect 😞')

        q = select(CardBase.learn_status) \
            .where(CardBase.back == back)
        old_learn_status = await query_to_db(q, async_session_maker)
        old_learn_status = old_learn_status.scalars().all()[0].value

        if old_learn_status != 0:
            new_learn_status = old_learn_status - 1

        status_enum = LearnStatusEnum(new_learn_status)

        q = update(CardBase) \
            .values(learn_status=status_enum) \
                .where(CardBase.user_id == str(message.from_user.id))
        await query_to_db(q, async_session_maker)
        await study_card_front(message=message,
                               card_num=card_num)
