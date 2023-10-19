#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 06:03:21 2023

@author: shbshka
"""
from aiogram import Bot, Dispatcher
import os
import pathlib
from dotenv import load_dotenv
from aiogram.fsm.storage.redis import RedisStorage
from aioredis import from_url

storage = RedisStorage(
    redis=from_url('redis://localhost:6379')
    )

path = pathlib.Path(__file__).parents[1]
load_dotenv(str(path) + '/.env')


bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(storage=storage)
