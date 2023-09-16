#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 00:05:24 2023

@author: shbshka
"""
from loader import bot, dp
from aiogram import types
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(equals='My profile 🥷'))
@dp.message_handler(commands=['/viewprofile'])
async def show_profile(message: types.Message):
    pass
