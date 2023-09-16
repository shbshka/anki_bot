#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:09:19 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram.dispatcher.filters import Text
import markups as nav


@dp.message_handler(Text(equals='Help 🤯'))
@dp.message_handler(commands=['help'])
async def send_help_message(message: types.Message):
    await bot.send_message(message.from_id,
                           '[insert instructions here]',
                           parse_mode='HTML', reply_markup=nav.help_menu)
