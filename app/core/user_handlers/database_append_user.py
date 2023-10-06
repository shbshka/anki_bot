#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 09:24:51 2023

@author: shbshka
"""
from loader import bot, dp

from aiogram import types
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from core.database.database_engine import async_session_maker
from core.database.database_models import UserBase
from core.database.database_commands import add_item_to_db

from typing import Dict, Any

import markups as nav


class NewUser(StatesGroup):
    introduction = State()
    name = State()
    surname = State()
    username = State()


@dp.message(F.text=='Cancel registration ⛔️')
async def cancel_registration(message: types.Message, state: FSMContext):

    """ Cancels the registration """

    await bot.send_message(message.from_user.id,
                           'Cancelled 💔',
                           reply_markup=nav.main_menu_anonymous \
                               .as_markup(resize_keyboard=True))
    await state.clear()


@dp.message(F.text=='Register 📋')
async def process_credentials(message: types.Message, state: FSMContext):

    """ Asks the user if they want to save their new or default credentials """

    await bot.send_message(message.from_user.id,
                           'Processing your information... 🕒',
                           reply_markup=nav.if_cancel  \
                               .as_markup(resize_keyboard=True))


    await state.update_data(username=message.from_user.username)
    await state.update_data(name=message.from_user.first_name)
    data = await state.update_data(surname=message.from_user.last_name)

    await bot.send_message(message.from_user.id,
                           f'Your name is: <b>{data["username"]}</b>\n'
                           f'Your surname is: <b>{data["name"]}</b>\n'
                           f'Your username is: <b>{data["surname"]}</b>\n\n'
                           ''
                           'Is that right?',
                           parse_mode='HTML',
                           reply_markup=nav.if_change_info \
                               .as_markup(resize_keyboard=True))
    await state.set_state(NewUser.introduction)


@dp.callback_query(F.call_data.startswith('if_change'))
@dp.callback_query(NewUser.introduction)
async def request_credentials(call: types.CallbackQuery, state: FSMContext):

    """
    Either adds the existing credentials to the database or invites
    the user to start entering their own ones provided that the user
    is not registred yet
    """

    data = await state.get_data()

    #add checking function here

    if call.data == 'if_change_no':
        await bot.send_message(call.from_user.id,
                               'Saving your information... 🕒')
        await call.message.delete()

        new_user = UserBase(telegram_id=str(call.from_user.id),
                        username=data['username'],
                        name=data['name'],
                        surname=data['surname'],
                        )
        await add_item_to_db(data=new_user, my_async_session=async_session_maker)
        await bot.send_message(call.from_user.id,
                               'You have been successfully registered! ✅',
                               reply_markup=nav.main_menu \
                                   .as_markup(resize_keyboard=True))

        await state.clear()

    elif call.data == 'if_change_yes':

        await state.clear()

        await bot.send_message(call.from_user.id,
                               'Please send your first name here 💬')
        await state.update_data(name=call.message.text)
        await call.message.delete()
        await state.set_state(NewUser.name)


@dp.message(NewUser.name)
async def process_name(message: types.Message, state: FSMContext):

    """ Retrieves name and asks for a surname """

    await state.update_data(name=message.text)
    data = await state.get_data()

    await bot.send_message(message.from_user.id,
                           f"Great, {data['name']}! Now send your second name 💬")
    await state.set_state(NewUser.surname)


@dp.message(NewUser.surname)
async def process_surname(message: types.Message, state: FSMContext):

    """ Retrieves surname and asks for a username """

    await state.update_data(surname=message.text)
    data = await state.get_data()

    await bot.send_message(message.from_user.id,
                           f"Thank you, {data['name']} {data['surname']}! What "
                           "username will you choose? 🤔")
    await state.set_state(NewUser.username)


@dp.message(NewUser.username)
async def process_username(message: types.Message, state: FSMContext):

    """
    Retrieves the username, checks if the username is unique and
    displays all the data with an invitation to confirm it
    """

    # добавить проверку на уникальность
    await state.update_data(username=message.text)
    data = await state.get_data()

    await bot.send_message(message.from_user.id,
                           'Processing your information... 🕒')
    await bot.send_message(message.from_user.id,
                           f'Your name is: <b>{data["name"]}</b>\n'
                           f'Your surname is: <b>{data["surname"]}</b>\n'
                           f'Your username is: <b>{data["username"]}</b>\n\n'
                           ''
                           'Is that right?',
                           parse_mode='HTML',
                           reply_markup=nav.if_change_info.as_markup())
    await state.set_state(NewUser.introduction)
