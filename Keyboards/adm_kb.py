from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton
import Database.db as db

adm_menu = InlineKeyboardMarkup(row_width=2)
# q = InlineKeyboardButton(text = 'Управление устройствами',callback_data='settings_phone')
#qw = InlineKeyboardButton(text = 'Выдать баланс',callback_data='givesum')
qq = InlineKeyboardButton(text = 'Выдать подписку ❌',callback_data='give_sub')
st = InlineKeyboardButton(text = 'Управление аккаунтами',callback_data='shopacc')
e = InlineKeyboardButton(text = 'Рассылка',callback_data='mailing')
r = InlineKeyboardButton(text = 'Статистика',callback_data='adm_stat')
t = InlineKeyboardButton(text = 'Меню гео',callback_data='SettingsGeo')
adm_menu.add(qq,st,e,r,t)



adm_menu_acc_shop = InlineKeyboardMarkup(row_width=2)
# q = InlineKeyboardButton(text = 'Управление устройствами',callback_data='settings_phone')
qw = InlineKeyboardButton(text = 'Выгрузить все аккаунты по разным txt',callback_data='outtxt')
qadd = InlineKeyboardButton(text = 'Добавление аккаунтов',callback_data='menuaddaccshop')
qq = InlineKeyboardButton(text = 'Меню управления',callback_data='menueditacc')
st = InlineKeyboardButton(text = 'Меню удаления',callback_data='menudeleteacc')
y = InlineKeyboardButton(text = 'Закрыть',callback_data='back_adm_panel')
adm_menu_acc_shop.add(qw,qadd,qq,st,y)

cancel_adm_acc_add = InlineKeyboardMarkup(row_width=1)
t = InlineKeyboardButton(text = 'Назад',callback_data='back_adm_panel')
cancel_adm_acc_add.add(t)

cancel_adm_give_sum = InlineKeyboardMarkup(row_width=1)
t = InlineKeyboardButton(text = 'Назад',callback_data='back_adm_panel')
cancel_adm_give_sum.add(t)

cancel_adm_kb = InlineKeyboardMarkup(row_width=1)
q = InlineKeyboardButton(text = 'Назад',callback_data='back')
cancel_adm_kb.add(q)

cancel_adm_kb_mailingg = InlineKeyboardMarkup(row_width=1)
q = InlineKeyboardButton(text = '🔙 Назад',callback_data='backmailing')
cancel_adm_kb_mailingg.add(q)

adm_add_geo = InlineKeyboardMarkup(row_width=1)
w = InlineKeyboardButton(text=f'Добавить новый гео', callback_data=f'addnewGEO')
r = InlineKeyboardButton(text=f'Редактировать гео', callback_data=f'editGEO')
t = InlineKeyboardButton(text=f'Удалить гео', callback_data=f'delGEO')
tt = InlineKeyboardButton(text=f'Назад', callback_data=f'back_adm_panel')
adm_add_geo.add(w,r,t,tt)

adm_menu_geo_back = InlineKeyboardMarkup(row_width=1)
# q = InlineKeyboardButton(text = 'Управление устройствами',callback_data='settings_phone')
backs = InlineKeyboardButton(text = 'Назад',callback_data='back_adm_panel')
adm_menu_geo_back.add(backs)

