from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton
'''import DataBase.db as db'''
import config


main_menu = ReplyKeyboardMarkup(row_width=3,resize_keyboard=True)
q = KeyboardButton(text = '👤 Профиль')
w = KeyboardButton(text = '🛒 Магазин')
r = KeyboardButton(text = '🖤 Купить подписку TikTokSoft')
e = KeyboardButton(text = '💌 Получить код с почты')
y = KeyboardButton(text = '🖤 Tik Tok Checker')
t = KeyboardButton(text = 'ℹ️ Информация')
it = KeyboardButton(text = '🗑 Корзина')
# r = KeyboardButton(text = 'Купить номер')
# t = KeyboardButton(text = 'Назад')
main_menu.add(q)
main_menu.add(w,r)
main_menu.add(e,y)
main_menu.add(it,t)

pass_mail_kb = InlineKeyboardMarkup(row_width=1)
w = InlineKeyboardButton(text = 'Назад',callback_data='cancel')
pass_mail_kb .add(w)