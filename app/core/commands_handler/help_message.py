#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:09:19 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram import F
from aiogram.filters import Command
import markups as nav


@dp.message(F.text=='Help 🤯')
@dp.message(Command('help'))
async def send_help_message(message: types.Message):
    await bot.send_message(message.from_user.id,
                           '[insert instructions here]',
                           parse_mode='HTML',
                           reply_markup=nav.help_menu.as_markup(resize_keyboard=True))
