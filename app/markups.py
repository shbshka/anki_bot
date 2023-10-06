#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:50:40 2023

@author: shbshka
"""
from aiogram.types import (ReplyKeyboardMarkup,
                           InlineKeyboardButton,
                           KeyboardButton,
                           InlineKeyboardMarkup)

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

#==========MAIN MENU==========
register = KeyboardButton(text='Register 📋')
send_help = KeyboardButton(text='Help 🤯')

main_menu_anonymous = ReplyKeyboardBuilder()
main_menu_anonymous.add(register, send_help)
main_menu_anonymous.adjust(2)

view_profile = KeyboardButton(text='My profile 🥷')
delete_account = KeyboardButton(text='Delete account 🗑')
send_help = KeyboardButton(text='Help 🤯')
show_cards = KeyboardButton(text='Cards 🃏')

main_menu = ReplyKeyboardBuilder()
main_menu.add(view_profile,
              delete_account,
              send_help,
              show_cards)
main_menu.adjust(2)


#==========CARD MENU==========
add_card = KeyboardButton(text='Add card 📝')
my_cards = KeyboardButton(text='My cards 📚')
edit_cards = KeyboardButton(text='Edit cards 🖊')
remove_card = KeyboardButton(text='Remove card 🗑')
study = KeyboardButton(text='Study 😵‍💫')
return_to_main_menu = KeyboardButton(text='Main Menu 🚪')

card_menu = ReplyKeyboardBuilder()
card_menu.add(add_card,
              my_cards,
              edit_cards,
              remove_card,
              study,
              return_to_main_menu)
card_menu.adjust(3)


#==========HELP MENU==========
how_register = InlineKeyboardButton(text='How to register',
                                       callback_data='how_register')
how_add_card = InlineKeyboardButton(text='How to add card',
                                    callback_data='how_add_card')
#continue here...

help_menu = InlineKeyboardBuilder()
help_menu.add(how_register,
              how_add_card)



#==========USER INFO PROCESSING==========

#changing info
if_change_no = InlineKeyboardButton(text='Yes!', callback_data='if_change_no')
if_change_yes = InlineKeyboardButton(text='No, I want to change it',
                                    callback_data='if_change_yes')

if_change_info = InlineKeyboardBuilder().add(if_change_no, if_change_yes)

#cancellation
cancel_card = KeyboardButton(text='Cancel card appending ⛔️')

if_cancel_card = ReplyKeyboardBuilder().add(cancel_card)


cancel_user = KeyboardButton(text='Cancel registration ⛔️')

if_cancel = ReplyKeyboardBuilder().add(cancel_user)
