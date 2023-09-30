#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 09:24:51 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from core.database.database_engine import async_session_maker
from core.database.database_models import UserBase
from core.database.database_commands import add_item_to_db
import markups as nav


class NewUser(StatesGroup):
    introduction = State()
    name = State()
    surname = State()
    username = State()


@dp.message_handler(Text(equals='Cancel ⛔️'), state="*")
async def cancel_registration(message: types.Message, state: FSMContext):

    """ Cancels the registration """

    await bot.send_message(message.from_id,
                           'Your registration has been cancelled 💔',
                           reply_markup=nav.main_menu_anonymous)
    await state.finish()


@dp.message_handler(Text(equals='Register 📋'))
async def process_credentials(message: types.Message, state: FSMContext):

    """ Asks the user if they want to save their new or default credentials """

    await bot.send_message(message.from_id,
                           'Processing your information... 🕒',
                           reply_markup=nav.if_cancel)

    async with state.proxy() as data:
        data['username'] = message.from_user.username
        data['name'] = message.from_user.first_name
        data['surname'] = message.from_user.last_name

        await bot.send_message(message.from_id,
                               f'Your name is: <b>{data["name"]}</b>\n'
                               f'Your surname is: <b>{data["surname"]}</b>\n'
                               f'Your username is: <b>{data["username"]}</b>\n\n'
                               ''
                               'Is that right?',
                               parse_mode='HTML',
                               reply_markup=nav.if_change_info)
    await state.set_state(NewUser.introduction)


@dp.callback_query_handler(lambda call: call.startswith('if_change'))
@dp.callback_query_handler(state=NewUser.introduction)
async def request_credentials(call: types.CallbackQuery, state: FSMContext):

    """
    Either adds the existing credentials to the database or invites
    the user to start entering their own ones provided that the user
    is not registred yet
    """

    #add checking function here

    if call.data == 'if_change_no':
        await bot.send_message(call.from_user.id,
                               'Saving your information... 🕒')
        await call.message.delete()

        async with state.proxy() as data:
            new_user = UserBase(telegram_id=str(call.from_user.id),
                            username=data['username'],
                            name=data['name'],
                            surname=data['surname'],
                            )
        await add_item_to_db(data=new_user, my_async_session=async_session_maker)
        await bot.send_message(call.from_user.id,
                               'You have been successfully registered! ✅',
                               reply_markup=nav.main_menu)

        await state.finish()

    elif call.data == 'if_change_yes':
        await bot.send_message(call.from_user.id,
                               'Please send your first name here 💬')
        await call.message.delete()
        await state.set_state(NewUser.name)


@dp.message_handler(state=NewUser.name)
async def process_name(message: types.Message, state: FSMContext):

    """ Retrieves name and asks for a surname """

    async with state.proxy() as data:
        data['name'] = message.text

    await bot.send_message(message.from_id,
                           f"Great, {data['name']}! Now send your second name 💬")
    await state.set_state(NewUser.surname)


@dp.message_handler(state=NewUser.surname)
async def process_surname(message: types.Message, state: FSMContext):

    """ Retrieves surname and asks for a username """

    async with state.proxy() as data:
        data['surname'] = message.text

    await bot.send_message(message.from_id,
                           f"Thank you, {data['name']} {data['surname']}! What "
                           "username will you choose? 🤔")
    await state.set_state(NewUser.username)


@dp.message_handler(state=NewUser.username)
async def process_username(message: types.Message, state: FSMContext):

    """
    Retrieves the username, checks if the username is unique and
    displays all the data with an invitation to confirm it
    """

    # добавить проверку на уникальность
    async with state.proxy() as data:
        data['username'] = message.text
    await bot.send_message(message.from_id,
                           'Processing your information... 🕒')
    await bot.send_message(message.from_id,
                           f'Your name is: <b>{data["name"]}</b>\n'
                           f'Your surname is: <b>{data["surname"]}</b>\n'
                           f'Your username is: <b>{data["username"]}</b>\n\n'
                           ''
                           'Is that right?',
                           parse_mode='HTML',
                           reply_markup=nav.if_change_info)
    await state.set_state(NewUser.introduction)
