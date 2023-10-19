#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 16:53:20 2023

@author: shbshka
"""
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def define_pagination(items, page, data_type, call_data):

    items = items.scalars().all()
    display_buttons = []

    for name in items:
        callback = f'{data_type}_callback ' + name
        button = InlineKeyboardButton(text=f'{name}',
                                          callback_data=f'{callback}')
        display_buttons.append(button)

    keyboard = InlineKeyboardBuilder()

    def button_splitter(buttons, n):
        for i in range(0, len(buttons), n):
            yield buttons[i: i + n]

    button_sets = list(button_splitter(display_buttons, 8))

    left = page - 1 if page != 1 else len(button_sets)
    right = page + 1 if page != len(button_sets) else 1

    left_button = InlineKeyboardButton(text='⬅️ back', callback_data=f'{data_type}_to_{left}_{call_data}')
    right_button = InlineKeyboardButton(text='forward ➡️', callback_data=f'{data_type}_to_{right}_{call_data}')
    page_button = InlineKeyboardButton(text=f'{str(page)}/{str(len(button_sets))}',
                                       callback_data='_')
    cancel_button = InlineKeyboardButton(text='Cancel ⛔️', callback_data=f'cancel_{data_type}')

    keyboard.add(
        left_button,
        page_button,
        right_button,
        cancel_button,
        )

    buttons = button_sets[page - 1]
    for button in buttons:
        keyboard.add(button)

    keyboard.adjust(3, 1, 4)


    return keyboard
