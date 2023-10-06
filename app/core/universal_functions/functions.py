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

    left_button = InlineKeyboardButton(text='⬅️back', callback_data=f'{data_type}_to_{left}_{call_data}')
    right_button = InlineKeyboardButton(text='forward➡️', callback_data=f'{data_type}_to_{right}_{call_data}')
    page_button = InlineKeyboardButton(text=f'{str(page)}/{str(len(button_sets))}',
                                       callback_data='_')
    cancel_button = InlineKeyboardButton(text='Cancel ⛔️', callback_data='cancel')

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


# @dp.callback_query(lambda call: call.data.startswith('to_'))
# async def set_callback_handler(call: CallbackData):
#     page = int(call.data.split('_')[1])
#     await call.message.delete()
#     await choose_set_for_removal(call.from_user.id, page=page)


# @dp.callback_query(lambda call: call.data.startswith('set_callback '))
# async def choose_card_for_removal(call, page=1):

#     #============INFO RETRIEVING=========

#     my_set = ' '.join(call.data.split(' ')[1::])

#     q = select(CardBase.name).where(CardBase.my_set == my_set)
#     cards_query = await retrieve_data_from_db(q, async_session_maker)
#     my_cards = cards_query.scalars().all()
#     cards_length = len(my_cards)

#     card_list = list()
#     for card in my_cards:
#         card_list.append(card)


#     #===============SWITCHERS============

#     left = page - 1 if page != 1 else cards_length
#     right = page + 1 if page != cards_length else 1

#     #==========CORE OF THE KEYBOARD=======

#     left_button = InlineKeyboardButton(text='⬅️back', callback_data=f'card_to_{left}')
#     right_button = InlineKeyboardButton(text='forward➡️', callback_data=f'card_to_{right}')
#     display_buttons = []

#     #===CHANGEABLE PART OF THE KEYBOARD===

#     for card_name in card_list:
#         card_callback = 'card_callback ' + card_name
#         card_button = InlineKeyboardButton(text=f'{card_name}',
#                                           callback_data=f'{card_callback}')
#         display_buttons.append(card_button)


#     #========BUILDING A KEYBOARD=========

#     cards = InlineKeyboardBuilder()

#     def button_splitter(buttons, n):
#         for i in range(0, len(buttons), n):
#             yield buttons[i: i + n]

#     button_cards = list(button_splitter(display_buttons, 8))
#     page_button = InlineKeyboardButton(text=f'{str(page)}/{str(len(button_cards))}',
#                                        callback_data='_')

#     cards.add(
#         left_button,
#         page_button,
#         right_button
#         )

#     buttons = button_cards[page - 1]
#     for button in buttons:
#         cards.add(button)

#     cards.adjust(3, 4)

#     await bot.send_message(call.from_user.id,
#                             'Which card do you want to remove?',
#                             reply_markup=cards.as_markup())


# @dp.callback_query(lambda call: call.data.startswith('card_to_'))
# async def card_callback_handler(call: CallbackData):
#     page = int(call.data.split('_')[2])
#     await call.message.delete()
#     await choose_card_for_removal(call, page=page)


# @dp.callback_query(lambda call: call.data.startswith('card_callback '))
# async def card_removal(call):
#     card_name = ' '.join(call.data.split(' ')[1::])

#     print(card_name)

#     q = delete(CardBase).where(CardBase.name == card_name)
#     await retrieve_data_from_db(q, async_session_maker)

#     await bot.send_message(call.from_user.id, 'The card has been deleted! ✅')
