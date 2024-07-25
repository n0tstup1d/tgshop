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

async def cart_pay(total_amount, number_check, user_id):
    kb = InlineKeyboardMarkup(row_width=2)
    e = InlineKeyboardButton(text = 'Оплатить💸', callback_data=f'bkt_{total_amount}_{number_check}_{user_id}')#callback_data=f'bk_{total_amount}_{number_check}_{user_id}')
    y = InlineKeyboardButton(text = 'Очистить корзину❌', callback_data='clearcart')
    # r = KeyboardButton(text = 'Купить номер')
    t = InlineKeyboardButton(text = 'Назад', callback_data='show_shop')
    kb.add(y,e)
    kb.add(t)
    return kb
async def cart_less_pay(total_amount, number_check, user_id, tips):
    kb = InlineKeyboardMarkup(row_width=2)
    e = InlineKeyboardButton(text = 'Оплатить💸', callback_data=f'tipbuy_{total_amount}_{number_check}_{user_id}_{tips}')#callback_data=f'bk_{total_amount}_{number_check}_{user_id}')
    y = InlineKeyboardButton(text = 'Очистить корзину❌', callback_data='clearcart')
    # r = KeyboardButton(text = 'Купить номер')
    t = InlineKeyboardButton(text = 'Назад', callback_data='show_shop')
    kb.add(y,e)
    kb.add(t)
    return kb

async def cart_less_format(total_amount, number_check, user_id):
    kb = InlineKeyboardMarkup(row_width=2)
    qw = InlineKeyboardButton(text='1️⃣', callback_data=f'for_1_{total_amount}_{number_check}_{user_id}')#_{country}')
    q = InlineKeyboardButton(text='2️⃣', callback_data=f'for_2_{total_amount}_{number_check}_{user_id}')#_{country}')
    w = InlineKeyboardButton(text='️3️⃣', callback_data=f'for_3_{total_amount}_{number_check}_{user_id}')#_{country}')
    r = InlineKeyboardButton(text='4️⃣', callback_data=f'for_3_{total_amount}_{number_check}_{user_id}')#_{country}')
    back = InlineKeyboardButton(text='Назад', callback_data=f'show_shop')
    kb.add(qw, q, w, r)
    kb.add(back)
    return kb

kb_shop_back = InlineKeyboardMarkup(row_width=1)
w = InlineKeyboardButton(text='Назад', callback_data='show_shop')
kb_shop_back.add(w)
kb_cart_shop = InlineKeyboardMarkup(row_width=1)
w = InlineKeyboardButton(text='Перейти к покупкам', callback_data='show_shop')
kb_cart_shop.add(w)
balance_kb = InlineKeyboardMarkup(row_width=1)
w = InlineKeyboardButton(text = 'Закрыть',callback_data='close')
balance_kb.add(w)

balance_kb = InlineKeyboardMarkup(row_width=1)
w = InlineKeyboardButton(text = 'Закрыть',callback_data='close')
balance_kb.add(w)


async def profile_payments_kb(sum, com):
    kb = InlineKeyboardMarkup(row_width=2)
    qw = InlineKeyboardButton(text='💚 LOLZ', callback_data=f'lolzpay_{sum}_{com}')
    q = InlineKeyboardButton(text = '🪙 USDT (CryptoBot)', callback_data=f'profile_pay_USDT_{sum}')
    w = InlineKeyboardButton(text = '⛏️ TRX (CryptoBot)', callback_data=f'profile_pay_TRX_{sum}')
    r = InlineKeyboardButton(text = '🔷 TON (CryptoBot)', callback_data=f'profile_pay_TON_{sum}')
    t = InlineKeyboardButton(text = 'Назад',callback_data='balance_add')
    kb.add(qw,q, w, r, t)
    return kb

async def time_otlega(geo, price ,c1,c2,c3,c4,c5):
    kb = InlineKeyboardMarkup(row_width=2)
    qw = InlineKeyboardButton(text='1️⃣', callback_data=f'tip_1_{geo}_{price}_{c1}')
    q = InlineKeyboardButton(text = '2️⃣', callback_data=f'tip_2_{geo}_{price}_{c2}')
    w = InlineKeyboardButton(text = '️3️⃣', callback_data=f'tip_3_{geo}_{price}_{c3}')
    r = InlineKeyboardButton(text = '4️⃣', callback_data=f'tip_4_{geo}_{price}_{c4}')
    t = InlineKeyboardButton(text = '5️⃣',callback_data=f'tip_5_{geo}_{price}_{c5}')
    back = InlineKeyboardButton(text='Назад', callback_data=f'show_shop')
    kb.add(qw,q, w, r, t)
    kb.add(back)
    return kb

async def write_cart(geo, count, tips):
    kb = InlineKeyboardMarkup(row_width=2)
    qw = InlineKeyboardButton(text='🔙 Назад', callback_data=f'f')
    q = InlineKeyboardButton(text='В корзину', callback_data=f'additemin_{geo}_{count}_{tips}')
    back = InlineKeyboardButton(text='❌ Отмена', callback_data=f'show_shop')
    kb.add(qw,q)
    kb.add(back)
    return kb

kb_pls = InlineKeyboardMarkup(row_width=2)
qw = InlineKeyboardButton(text='🔙 Назад', callback_data=f'f')
q = InlineKeyboardButton(text='В корзину', callback_data=f'additemin')
back = InlineKeyboardButton(text='❌ Отмена', callback_data=f'show_shop')
kb_pls.add(qw,q)
kb_pls.add(back)



async def profile_buyments_kb(price, com, number_check, user_id, tips):
    kb = InlineKeyboardMarkup(row_width=2)
    qw = InlineKeyboardButton(text='💚 LOLZ',callback_data=f'lolzbuy_{price}_{com}_{number_check}_{user_id}_{tips}')
    q = InlineKeyboardButton(text = '🪙 USDT (CryptoBot)', callback_data=f'profile_buy_USDT_{price}_{number_check}_{user_id}_{tips}')
    w = InlineKeyboardButton(text = '⛏️ TRX (CryptoBot)', callback_data=f'profile_buy_TRX_{price}_{number_check}_{user_id}_{tips}')
    r = InlineKeyboardButton(text = '🔷 TON (CryptoBot)', callback_data=f'profile_buy_TON_{price}_{number_check}_{user_id}_{tips}')
    t = InlineKeyboardButton(text = 'Назад',callback_data='balance_add')
    kb.add(qw,q, w, r, t)
    return kb


'''async def shop_acc_kb(region, price, count):
    kb = InlineKeyboardMarkup(row_width=2)
    r = InlineKeyboardButton(text='Добавить в корзину 🛒', callback_data=f'additemincart_{region}_{price}_{count}')
    #q = InlineKeyboardButton(text='Оплатить 💸', callback_data=f'buy_{region}_{price}_{count}')
    w = InlineKeyboardButton(text='Назад', callback_data='cancel_mail')
    kb.add(r)
    kb.add(w)
    return  kb'''
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
            async with db.DatabaseBot("DataBase/db.db") as db_bot:
                counss = await db_bot.get_count_geo(country)
            async with db.DatabaseBot("DataBase/db.db") as db_bot:
                couns = await db_bot.get_names_countries_acc(country)
            q = InlineKeyboardButton(text=f'{couns} | {counss} шт.| {rr} ₽', callback_data=f'accbuy_{country}_{rr}')
            kb.add(q)
    return kb
