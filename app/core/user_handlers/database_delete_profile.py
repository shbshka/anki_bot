#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 18:54:07 2023

@author: shbshka
"""
from loader import bot, dp

from aiogram import types
from aiogram import F
from aiogram.filters import Command

import markups as nav


@dp.message(F.text == "Delete account 🗑")
@dp.message(Command('deleteaccount'))
async def delete_profile(message: types.message):
    await bot.send_message(message.from_user.id,
                           'Temporarily unavailable :(')
