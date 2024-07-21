from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton
import Database.db as db

adm_menu = InlineKeyboardMarkup(row_width=2)
# q = InlineKeyboardButton(text = 'Управление устройствами',callback_data='settings_phone')
qw = InlineKeyboardButton(text = 'Выдать баланс',callback_data='givesum')
qq = InlineKeyboardButton(text = 'Выдать подписку',callback_data='give_sub')
st = InlineKeyboardButton(text = 'Добавить аккаунты',callback_data='shop_')
e = InlineKeyboardButton(text = 'Рассылка',callback_data='mailing')
r = InlineKeyboardButton(text = 'Статистика',callback_data='adm_stat')
t = InlineKeyboardButton(text = 'Гео',callback_data='SettingsGeo')
i = InlineKeyboardButton(text = 'Язык',callback_data='SettingsLang')
u = InlineKeyboardButton(text = 'Изменить версию',callback_data='change_version')
y = InlineKeyboardButton(text = 'Закрыть',callback_data='close')
adm_menu.add(qw,qq,st,e,r,t,i,u,y)

cancel_adm_give_sum = InlineKeyboardMarkup(row_width=1)
t = InlineKeyboardButton(text = 'Назад',callback_data='back_in_geo')
cancel_adm_give_sum.add(t)