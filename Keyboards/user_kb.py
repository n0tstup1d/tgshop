from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton
import Database.db as db
import config


main_menu = ReplyKeyboardMarkup(row_width=3,resize_keyboard=True)
q = KeyboardButton(text = '👤 Профиль')
w = KeyboardButton(text = '🛒 Магазин')
r = KeyboardButton(text = '🖤 Меню подписки')
t = KeyboardButton(text = 'ℹ️ Информация')
it = KeyboardButton(text = '🗑 Корзина')
# r = KeyboardButton(text = 'Купить номер')
# t = KeyboardButton(text = 'Назад')
main_menu.add(q)
main_menu.add(w,r)
main_menu.add(it,t)


main_menu_sub = InlineKeyboardMarkup(row_width=2)
e = InlineKeyboardButton(text = '💌 Получить код с почты', callback_data='codemail')
y = InlineKeyboardButton(text = '🖤 Tik Tok Checker', callback_data='tiktokchecker')
# r = KeyboardButton(text = 'Купить номер')
t = InlineKeyboardButton(text = 'Назад', callback_data='backsub')
main_menu_sub.add(e,y)
main_menu_sub.add(t)
async def mail_back_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    w = InlineKeyboardButton(text='Назад', callback_data='cancel_mail')
    kb.add(w)
    return kb

async def shop_menu_acc():
    kb = InlineKeyboardMarkup(row_width=1)

    country_count = {}
    with open('accounts.txt', 'r') as file:
        for line in file:
            if line.strip():  # Проверяем, что строка не пустая
                country_code = line.split(':')[0]
                if country_code in country_count:
                    country_count[country_code] += 1
                else:
                    country_count[country_code] = 1
    async with db.DatabaseBot("DataBase/db.db") as db_bot:
        couns = await db_bot.get_countries_acc()
    country_rr_map = {row[0]: row[1] for row in couns}
    for country, count in country_count.items():
        if country in country_rr_map:
            rr = country_rr_map[country]
            print(country)
            q = InlineKeyboardButton(text=f'{country} | {count} шт.| {rr} $', callback_data=f'AccBuy_{country}_{rr}{country}_{rr}')
            kb.add(q)

    w = InlineKeyboardButton(text='Закрыть', callback_data='close')
    kb.add(w)
    return kb
