#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:50:40 2023

@author: shbshka
"""
from aiogram.types import (inline_keyboard_button,
                           inline_keyboard_markup,
                           keyboard_button,
                           reply_keyboard_markup)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

#==========MAIN MENU==========
register = KeyboardButton(text='Register 📋')
send_help = KeyboardButton(text='Help 🤯')

main_menu_anonymous = ReplyKeyboardBuilder().add(register,
                                                 send_help)

view_profile = KeyboardButton(text='My profile 🥷')
delete_account = KeyboardButton(text='Delete account 🗑')
send_help = KeyboardButton(text='Help 🤯')
show_cards = KeyboardButton(text='Cards 🃏')

main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(view_profile,
                                                          delete_account,
                                                          show_cards,
                                                          send_help)


#==========CARD MENU==========
add_card = KeyboardButton(text='Add card 📝')
my_cards = KeyboardButton(text='My cards 📚')
edit_cards = KeyboardButton(text='Edit cards 🖊')
remove_card = KeyboardButton('Remove card 🗑')
return_to_main_menu = KeyboardButton(text='Main Menu 🚪')

card_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(add_card,
                                                          my_cards,
                                                          edit_cards,
                                                          remove_card,
                                                          return_to_main_menu)


#==========HELP MENU==========
how_to_register = InlineKeyboardButton(text='How to register',
                                       callback_data='how_to_register')
how_add_card = InlineKeyboardButton(text='How to add card',
                                    callback_data='how_add_card')
#continue here...

help_menu = InlineKeyboardMarkup().add(how_to_register,
                                       how_add_card) #add the rest...


#==========USER INFO PROCESSING==========

#changing info
if_change_no = InlineKeyboardButton('Yes!', callback_data='if_change_no')
if_change_yes = InlineKeyboardButton('No, I want to change it',
                                    callback_data='if_change_yes')

if_change_info = InlineKeyboardMarkup().add(if_change_no, if_change_yes)

#cancellation
cancel = KeyboardButton('Cancel ⛔️')

if_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(cancel)
