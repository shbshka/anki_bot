#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 13:38:43 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram.dispatcher.filters import Text

import markups as nav


@dp.message_handler(Text(equals='Cards 🃏'))
@dp.message_handler(commands=['cards'])
async def cards_menu(message: types.Message):
    await bot.send_message(message.from_id,
                           'Here are your cards, Learner! 🤓',
                           reply_markup=nav.card_menu)


@dp.message_handler(Text(equals='Main Menu 🚪'))
@dp.message_handler(commands=['main_menu'])
async def return_to_main_menu(message: types.Message):
    await bot.send_message(message.from_id,
                           'Returning to Main Menu... 🕒',
                           reply_markup=nav.main_menu)
