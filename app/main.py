#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 06:03:14 2023

@author: shbshka
"""
import asyncio
from core import dp
from loader import bot

from core.database.database_models import init_models

import nest_asyncio
nest_asyncio.apply()


async def run():
    asyncio.run(init_models())
    await dp.start_polling(bot)


loop = asyncio.get_event_loop()


if __name__ == '__main__':
    loop.run_until_complete(run())
