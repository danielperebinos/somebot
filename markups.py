from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_menu = InlineKeyboardMarkup(row_width=2)

yes_button = InlineKeyboardButton(text = 'Yes', callback_data='yes')
no_button = InlineKeyboardButton(text = 'No', callback_data='no')

start_menu.insert(yes_button)
start_menu.insert(no_button)

skip_menu = InlineKeyboardMarkup(row_width=1)
skip_button = InlineKeyboardButton(text = 'Skip', callback_data='skip')
skip_menu.insert(skip_button)

