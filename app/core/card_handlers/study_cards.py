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

import markups as nav


@dp.message(F.text=='Study 😵‍💫')
@dp.message(Command('study'))
async def select_set(message: types.Message, state: FSMContext):

    """ Selects the set that is required to be studied """




@dp.message(F.text=='Finish studying ✅')
async def cancel_studying(message: types.Message, state: FSMContext):

    """ Cancels studying """

    await bot.send_message(message.from_user.id,
                           'Studying completed! ✅',
                           reply_markup=nav.card_menu \
                               .as_markup(resize_keyboard=True))
    await state.clear()
