#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 13:38:43 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram import F
from aiogram.filters import Command

import markups as nav


@dp.message(F.text=='Cards 🃏')
@dp.message(Command('cards'))
async def cards_menu(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Here are your cards, Learner! 🤓',
                           reply_markup=nav.card_menu.as_markup(resize_keyboard=True))


@dp.message(F.text=='Main Menu 🚪')
@dp.message(Command('main_menu'))
async def return_to_main_menu(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Returning to Main Menu... 🕒',
                           reply_markup=nav.main_menu.as_markup(resize_keyboard=True))
