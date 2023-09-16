#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:50:40 2023

@author: shbshka
"""
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           KeyboardButton,
                           ReplyKeyboardMarkup)

#==========MAIN MENU==========
register = KeyboardButton('Register 📋')
send_help = KeyboardButton('Help 🤯')

main_menu_anonymous = ReplyKeyboardMarkup(resize_keyboard=True).add(register,
                                                                    send_help)

view_profile = KeyboardButton('My profile 🥷')
delete_accout = KeyboardButton('Delete account 🗑')
send_help = KeyboardButton('Help 🤯')
show_cards = KeyboardButton('Cards 🃏')

main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(view_profile,
                                                          delete_accout,
                                                          show_cards,
                                                          send_help)


#==========CARD MENU==========
add_card = KeyboardButton('Add card 📝')
my_cards = KeyboardButton('My cards 📚')
edit_cards = KeyboardButton('Edit cards 🖊')
remove_card = KeyboardButton('Remove card 🗑')

card_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(add_card,
                                                          my_cards,
                                                          edit_cards,
                                                          remove_card)


#==========HELP MENU==========
how_add_card = InlineKeyboardButton('How to add card',
                                    callback_data='how_add_card')
#continue here...

help_menu = InlineKeyboardMarkup().add(how_add_card) #add the rest...


#==========USER INFO PROCESSING==========

#changing info
if_change_no = InlineKeyboardButton('Yes!', callback_data='if_change_no')
if_change_yes = InlineKeyboardButton('No, I want to change it',
                                    callback_data='if_change_yes')

if_change_info = InlineKeyboardMarkup().add(if_change_no, if_change_yes)

#cancellation
cancel = KeyboardButton('Cancel ⛔️')

if_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(cancel)
