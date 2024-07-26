from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils import executor
from aiogram.types import ParseMode
from LOLZTEAM import AutoUpdate, Constants
from LOLZTEAM.API import Forum, Market
from LOLZTEAM.Tweaks import DelaySync, SendAsAsync, CreateJob
from LOLZTEAM.Utils import CheckPayment
from LOLZTEAM.API import Market
from config import token_lolz
import string
import json
import requests
from aiogram.utils import markdown as md
import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from datetime import date, datetime, timedelta
import Database.db as db
import config
import Keyboards.user_kb as user_kb
import Keyboards.adm_kb as adm_kb
import Payments.cryptobot as cryptobot
import Keyboards.user_kb as user_kb
import BotCommands.commands as commands
import states
import traceback
import random
import os
import rarfile
import zipfile
import asyncio
import shutil
import multiprocessing
'''import other.upload_files as upload_files
import tiktok.MainTikTok as MainTikTok
import tiktok.MainTikTokCircle as MainTikTokCircle'''
import logging
import time
from concurrent.futures import ThreadPoolExecutor
'''import other.dowload_files as dowload_files'''



def random_string(length):
    letters = string.ascii_letters  # Строка из всех букв латинского алфавита (нижний и верхний регистр)
    return ''.join(random.choice(letters) for _ in range(length))


async def delete_old_items_periodically():
    while True:
        print(f'Начало очистки в {datetime.today()}')
        async with db.DatabaseBot("Database/db.db") as db_bot:
            tems = await db_bot.get_old_items()
            if tems:  # Проверка, что список не пуст
                tems_json_str = tems[0]
                        # Преобразуем JSON-строку обратно в список Python
                tems_list = json.loads(tems_json_str)
                # Выводим список в нужном формате
                print(tems_list)
                for value in tems_list:
                    print(value)
                    parts = value
                    tt = parts.split(':')
                    print(tt[0])
                    geo = tt[0]
                    async with db.DatabaseBot("Database/db.db") as db_bot:
                        await db_bot.insert_account(geo, value)

                async with db.DatabaseBot("Database/db.db") as db_bot:
                    await db_bot.delete_old_items()
            else:
                print('Корзины пусты')
        print(f"Очистка корзины окончена в {datetime.today()}")
        await asyncio.sleep(120)  # Ожидаем 30 минут

def extract_accounts(country_code, count):
    tag = count
    with open('accounts.txt', 'r') as file:
        lines = file.readlines()

    # Отфильтровать строки по тегу
    extracted_lines = [line for line in lines if line.startswith(tag)]
    count = int(count)

    # Выбрать только необходимые строки для удаления
    to_remove = extracted_lines[:count]

    # Удалить выбранные строки из списка всех строк
    remaining_lines = []
    removed_count = 0

    for line in lines:
        if line.startswith(tag) and removed_count < count:
            removed_count += 1
            continue
        remaining_lines.append(line)

    # Перезаписать файл с оставшимися строками
    with open('accounts.txt', 'w') as file:
        file.writelines(remaining_lines)

    # Вернуть вырезанные строки
    return to_remove
def extract_lines(tag, count):
    with open('accounts.txt', 'r') as file:
        lines = file.readlines()

    # Отфильтровать строки по тегу
    extracted_lines = [line for line in lines if line.startswith(tag)]
    to_remove = extracted_lines[:int(count)]

    # Удалить выбранные строки из списка всех строк
    remaining_lines = [line for line in lines if line not in to_remove]

    # Перезаписать файл с оставшимися строками
    with open('accounts.txt', 'w') as file:
        file.writelines(remaining_lines)

    # Вернуть вырезанные строки
    return to_remove


# Настройка базового логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Создание логгера
logger = logging.getLogger(__name__)

# Пример использования логирования
logger.info('Бот запускается')


bot = Bot(token=config.bot_token, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

market = Market(token=token_lolz, language="ru")
forum = Forum(token=token_lolz, language="ru")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    arg = message.get_args()
    print(arg)
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    format = yesterday.strftime('%Y-%m-%d')
    await commands.set_default_commands(bot)
    async with db.DatabaseBot("Database/db.db") as db_bot:
        rez = await db_bot.check_users_start(message.from_user.id)
    if rez:
        pass
    else:
        current_date = date.today()
        async with db.DatabaseBot("Database/db.db") as db_bot:
            await db_bot.insert_user(message.from_user.id, current_date, format)
    await bot.send_message(message.chat.id, text='Добро пожаловать', reply_markup=user_kb.main_menu)


@dp.message_handler(commands=['adm'])
async def adm(message:types.Message):
    if message.from_user.id in config.id_adm:
        await bot.send_message(message.chat.id,text = 'Добро пожаловать в админ панель', reply_markup=adm_kb.adm_menu)#reply_markup=adm_kb.adm_menu


@dp.message_handler(content_types=['text'])
async def text(message:types.Message):
    if message.text == "👤 Профиль":
        async with db.DatabaseBot("Database/db.db") as db_bot:
            user_info = await db_bot.get_user_bal(message.chat.id)
        await bot.send_message(message.chat.id, f"👤 Ваш ID: `{message.chat.id}`\n\n"
                                                f"💕 Купленных акаунтов: {user_info}"
                                                #f"\n"
                                               # f"Куплено аккаунтов: бд нет\n"
                                                #f"Может сделать на все товары как написанно выше "
                                                , parse_mode='Markdown')
    if message.text == "🛒 Магазин":
        '''async with db.DatabaseBot("Database/bd.db") as db_bot:
            res = await db_bot.get_accont()'''
        await bot.send_message(message.chat.id, f"---------------- В наличии ----------------\n",
                                                reply_markup=await user_kb.shop_menu_acc())

        print()

    if message.text == "ℹ️ Информация":
        await bot.send_message(message.chat.id,
                                                "\n"
                                                "Тут могут быть ссылки на чаты"
                                                "\n"
                                                "Возникли вопросы по работе магазина писать в тех. поддержку\n"
                                                "Тех.поддержка: None\n"
                                                "\n"
                                                "Если возникли проблемы с товаром магазина, писать админу"
                                                "Связь с администратором: None\n")
    if message.text == "🗑 Корзина":
        print(message.from_user.id)
        async with db.DatabaseBot("Database/db.db") as db_bot:
            id_cart = await db_bot.get_id_cart(message.chat.id)
        async with db.DatabaseBot("Database/db.db") as db_bot:
            items = await db_bot.get_items(message.chat.id)
        print(f"{items}\n↑ items")
        total_amount = 0.0
        # Итерация по каждому кортежу
        for item in items:
            id_value, country, amount = item
            # Сложение amount
            total_amount += amount

        # Печать суммы всех amount
        response_text = ""
        if items:
            total_amount = 0
            # Извлечение значения
            number_check = str(id_cart[0][0])
            user_id = message.chat.id
            response_text = (f"Номер вашего заказа: `{str(id_cart[0][0])}`\n\n"
                             f"Ваша корзина:\n")
            for item in items:
                id_value, country, amount = item
                #print(f"Обработанный элемент: Количество={id_value}, Страна={country}, Сумма={amount}, Текущая общая сумма={total_amount}")
                response_text += (f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                  f"Страна {country} | {id_value} шт. | {amount} ₽\n"
                                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n")
                total_amount += amount

            response_text += f"\nСумма к оплате: {total_amount} ₽ "

            await message.answer(response_text, parse_mode='Markdown', reply_markup=await user_kb.cart_pay(total_amount, number_check, user_id))
        else:
            await bot.send_message(message.chat.id, "🛒 Корзина пуста", reply_markup=user_kb.kb_cart_shop)
        '''await bot.send_message(message.chat.id,"Введите вашу почту", reply_markup=await user_kb.mail_back_kb())
        await states.user_states.for_maill.set()'''

    if message.text == '🖤 Меню подписки':
        async with db.DatabaseBot("Database/db.db") as db_bot:
            rez = await db_bot.check_users_sub(message.from_user.id)
            print(rez)
        today = datetime.today()
        formatted_date = today.strftime('%Y-%m-%d')
        if rez < formatted_date:
            await bot.send_message(message.chat.id,"🛠 В разработке 🛠"
                                                #"__У вас отсутвует подписка__ 😕\n"
                                                #"\n"
                                                #"При покупки подписки вы получаете:\n\n"
                                                #"♦ Тик Ток Чекер 🖤\n"
                                                #"♦ Получение кодов от почты 💌\n"
                                                #"♦ Уникализатор видео и фото 🖼"
                                   ,  parse_mode=ParseMode.MARKDOWN_V2 ,reply_markup=await user_kb.mail_back_kb())
        else:
            async with db.DatabaseBot("Database/db.db") as db_bot:
                mon = await db_bot.check_users_mon(message.from_user.id)
            await bot.send_message(message.chat.id,
                                   "Добро пожаловать\n"
                                   "\n"
                                   f"Ваша подписка действует до:{rez}\n\n"
                                   f"Ваш баланс{float(mon)}", parse_mode=ParseMode.MARKDOWN_V2,
                                   reply_markup=await user_kb.mail_back_kb())

@dp.callback_query_handler()
async def call(call: CallbackQuery):
    if call.data == 'givesum':
        await bot.edit_message_text('Введите id пользователя, которому хотите пополнить баланс.',
                                    call.message.chat.id, call.message.message_id,
                                    reply_markup=adm_kb.cancel_adm_give_sum)
        await states.adm_states.get_sum_id.set()
    elif call.data == 'shopacc':
        message = 'Список существующих стран в магазине и их список:\n'
        async with db.DatabaseBot("Database/db.db") as db_bot:
            contrys = await db_bot.get_count_acc()
        for value in contrys:
            async with db.DatabaseBot("Database/db.db") as db_bot:
                count = await db_bot.get_count_acc_sum(value[0])
            print(f"{value[0]} | {count[0][0]}")
            message += f"{value[0]} | {count[0][0]}\n"
        await bot.edit_message_text(message, call.message.chat.id, call.message.message_id,
                                reply_markup=adm_kb.adm_menu_acc_shop)

    elif call.data == 'SettingsGeo':
        async with db.DatabaseBot("Database/db.db") as db_bot:
            countries = await db_bot.get_countries_acc()
        message = "Список гео:\n"
        if countries:
            for region, price, names in countries:
                message += f"Название {str(names)}: Регион {region}: Стоимость {price} ₽\n"
            await bot.edit_message_text(message, call.message.chat.id, call.message.message_id,
                                        reply_markup=adm_kb.adm_add_geo)
        else:
            await bot.edit_message_text('Тут должен быть список гео, но пока гео нет(', call.message.chat.id, call.message.message_id,
                                        reply_markup=adm_kb.adm_add_geo)


    elif call.data == 'addnewGEO':
        async with db.DatabaseBot("Database/db.db") as db_bot:
            countries = await db_bot.get_countries_acc()
        if countries:
            message = ('Введите новое гео капсом:\n'
                       'Существующие:\n')
            for region, price, names in countries:
                message += f"Название {str(names)}: Регион {region}: Стоимость {price} ₽\n"
            await bot.edit_message_text(message, call.message.chat.id, call.message.message_id,
                                        reply_markup=adm_kb.adm_add_geo)
        else:
            message = 'В базе данных нет информации о странах.'
        await bot.edit_message_text(message,call.message.chat.id,call.message.message_id,reply_markup=adm_kb.adm_menu_geo_back)
        await states.adm_states.input_new_geo_sum.set()

    elif call.data == 'delGEO':
        async with db.DatabaseBot("Database/db.db") as db_bot:
            countries = await db_bot.get_countries_acc()
        if countries:
            message = ('Введите гео которое хотите удалит:\n'
                       'Существующие:\n')
            for region, price, names in countries:
                message += f"Название {str(names)}: Регион {region}: Стоимость {price} ₽\n"
            await bot.edit_message_text(message, call.message.chat.id, call.message.message_id,
                                        reply_markup=adm_kb.adm_add_geo)
        else:
            message = 'В базе данных нет информации о странах.'
        await bot.edit_message_text(message,call.message.chat.id,call.message.message_id,reply_markup=adm_kb.adm_menu_geo_back)
        await states.adm_states.input_del_geo_sum.set()

    elif call.data == 'back_adm_panel':
        await bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text='Админ панель', reply_markup=adm_kb.adm_menu)

    elif call.data == 'back':
        await bot.edit_message_text('Выберите нужные настройки', call.message.chat.id, call.message.message_id,
                                reply_markup=adm_kb.adm_menu)

    elif call.data == 'mailing':
        await bot.edit_message_text('Отправьте сообщение для рассылки', call.message.chat.id, call.message.message_id,
                                    reply_markup=adm_kb.cancel_adm_kb_mailingg)
        await states.adm_states.mailing.set()

    elif call.data == 'editGEO':
        async with db.DatabaseBot("Database/db.db") as db_bot:
            countries = await db_bot.get_countries_acc()
        if countries:
            message = ('Введите гео капсом которое хотите отредактировать:\n'
                       'Существующие:\n')
            for country in countries:
                message += f'Название: {country[0]}, Цена: {country[1]} ₽\n'
        else:
            message = 'В базе данных нет информации о странах.'
        await bot.edit_message_text(message,call.message.chat.id,call.message.message_id,reply_markup=adm_kb.adm_menu_geo_back)
        await states.adm_states.input_new_geo_sum_for_edit.set()


    elif call.data == 'menuaddaccshop':
        await bot.edit_message_text('Скиньте файл (.txt) с аккаунтами (можно с разными гео)', call.message.chat.id, call.message.message_id ,reply_markup=adm_kb.adm_menu_geo_back)
        await states.adm_states.get_shop_acc.set()

    elif call.data == 'balance_add':
        await bot.edit_message_text('Введите сумму для пополнения в ₽',call.message.chat.id,call.message.message_id,reply_markup=adm_kb.cancel_adm_kb)
        await states.user_states.new_balance.set()

    elif call.data.startswith('tip_'):
        tips = call.data.split('_')[1]
        geo = call.data.split('_')[2]
        price = call.data.split('_')[3]
        counts_acc_time = call.data.split('_')[4]
        if tips == '1':
            otlega = 'меньше 4ч'
        elif tips == '2':
            otlega = 'больше 4ч'
        elif tips == '3':
            otlega = 'больше 12ч'
        elif tips == '4':
            otlega = 'больше 24ч'
        elif tips == '5':
            otlega = 'больше 36ч'
        async with db.DatabaseBot("Database/db.db") as db_bot:
            counts = await db_bot.get__geo(geo)
        async with db.DatabaseBot("Database/db.db") as db_bot:
            count = await db_bot.get_count_geo(geo)
        countuser = int(1)
        message = (
            f"Регион: {geo}\nОтлежка: {otlega}\n\n"
            f"⬇️Укажите количество аккаунтов сообщением⬇️\n"
            f"<strong>(просто отправьте цифру в чат)!</strong>\n\n"
            f"<u>Если Вы ошиблись, цифру можно ввести повторно🔄</u>\n\n"
            f"✅ Доступно к покупке: {counts_acc_time} шт.\n\n"
            f"🛒 Количество: {int(countuser)} шт. \n\n"

        )

        await bot.edit_message_text(message, call.message.chat.id, call.message.message_id,
                                    reply_markup=await user_kb.write_cart(geo, int(countuser), int(tips), price))
        await states.user_states.new_acc_buy.set()
        state = Dispatcher.get_current().current_state()
        await state.update_data(geo=geo)
        await state.update_data(price=price)
        await state.update_data(tipst=tips)
        await state.update_data(count=countuser)
        await state.update_data(message_id=call.message.message_id)

        '''await states.user_states.new_acc_buy.set()
        state = Dispatcher.get_current().current_state()
        await state.update_data(geo=geo)
        await state.update_data(price=price)'''

        '''await bot.edit_message_text('Введите кол-во аккаунтов',call.message.chat.id,call.message.message_id,reply_markup=user_kb.kb_shop_back)

        '''

    elif call.data.startswith('accbuy_'):
        geo = call.data.split('_')[1]
        price = call.data.split('_')[2]
        '''async with db.DatabaseBot("Database/db.db") as db_bot:
            count_geo = await db_bot.get_count_geo(geo)'''
        ''' message = f"Регион: {geo}\n ⬇️⬇️Доступно к покупке⬇️⬇️\n \nВсего: {count_geo} шт.\n"'''
        async with db.DatabaseBot("Database/db.db") as db_bot:
            counts = await db_bot.get__geo(geo)
        message = (
            f"Регион: {geo}\n ⬇️⬇️Доступно к покупке⬇️⬇️\n \n"
            f"1️⃣ - Отлежка меньше 4ч: {counts['less_4h']} шт.\n\n"
            f"2️⃣ - Отлежка больше 4ч: {counts['more_4h_less_12h']} шт.\n\n"
            f"3️⃣ - Отлежка больше 12ч: {counts['more_12h_less_24h']} шт.\n\n"
            f"4️⃣ - Отлежка больше 24ч: {counts['more_24h_less_36h']} шт.\n\n"
            f"5️⃣ - Отлежка больше 36ч: {counts['more_36h']} шт."
        )
        c1 = int(counts['less_4h'])
        c2 = int(counts['more_4h_less_12h'])
        c3 = int(counts['more_12h_less_24h'])
        c4 = int(counts['more_24h_less_36h'])
        c5 = int(counts['more_36h'])
        await bot.edit_message_text(message, call.message.chat.id, call.message.message_id,
                                    reply_markup=await user_kb.time_otlega(geo, price,c1,c2,c3,c4,c5))
        '''await states.user_states.new_acc_buy.set()
        state = Dispatcher.get_current().current_state()
        await state.update_data(geo=geo)
        await state.update_data(price=price)'''
        '''await bot.edit_message_text('Введите кол-во аккаунтов',call.message.chat.id,call.message.message_id,reply_markup=user_kb.kb_shop_back)
        
        
        
        '''
    elif call.data.startswith('clearcart'):
        item = call.message.get_args()
        print(call.message.chat.id)
        async with db.DatabaseBot("Database/db.db") as db_bot:
            tems = await db_bot.get_item(call.message.chat.id)
        print(tems)
        for idx, item in enumerate(tems):
            it = item[0]
            cleaned_string = it.strip("[]'")
            cleaned_string = cleaned_string.replace("\\n", "\n").replace("', '", "\n")
            cleanedd_string = "\n".join([line.strip() for line in cleaned_string.splitlines() if line.strip()])
            print(cleanedd_string)

            cleanedt_text = cleanedd_string.strip('"')

            # Replace comma and space with a newline character
            cleaneds_text = cleanedt_text.replace('", "', '\n')
            lines = cleaneds_text.split('\n')
            print(lines)
            t = 0
            for value in lines:
                print(lines[t])
                parts = lines[t]
                tt = parts.split(':')
                geo = tt[0]
                print(geo)
                async with db.DatabaseBot("Database/db.db") as db_bot:
                    await db_bot.insert_account(geo,lines[t])
                t += 1
        async with db.DatabaseBot("Database/db.db") as db_bot:
            await db_bot.delete_item(call.message.chat.id)
        await bot.edit_message_text(f"Корзина очищена ❌",call.message.chat.id, call.message.message_id)
    elif call.data.startswith('show_shop'):
        await bot.edit_message_text(f"---------------- В наличии ----------------\n",call.message.chat.id, call.message.message_id,
                               reply_markup=await user_kb.shop_menu_acc())

    elif call.data.startswith('lolzbuy_'):
        suma = call.data.split('_')[1]
        rubles = float(suma)
        com = call.data.split('_')[2]
        print(com)
        num_check = call.data.split('_')[3]
        user_id = call.data.split('_')[4]
        tips = call.data.split('_')[5]
        print(tips)
        url_lolz=str(market.payments.generate_link(username='notstupid', user_id='7591946', comment=com, currency=Constants.Market.Currency.rub, amount=rubles))
        kb = InlineKeyboardMarkup(row_width=1)
        q = InlineKeyboardButton(text='Перейти к оплате', url=url_lolz)
        qq = InlineKeyboardButton(text='Проверить оплату', callback_data=f'check_lolzbuy_{rubles}_{com}_{num_check}_{user_id}_{tips}')
        w = InlineKeyboardButton(text='Отменить', callback_data=f'cancel_order')
        kb.add(q,qq,w)
        await bot.edit_message_text(f'🆙 Пополнение баланса\n'
                                    f'➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                    f'🤖 Для пополнения баланса, нажмите на кнопку ниже.\n'
                                    f'➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                    f'❗Не изменять коммент❗\n'
                                    f'‼После оплаты, обязательно нажмите проверить оплату‼\n' #https://lzt.market/balance/transfer?username=ChivapChiCH&hold=0&amount=7&comment=1719910189.48956_cf0496c474
                                    '➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                    f'💰 Сумма пополнения: {suma} ₽\n'
                                    '➖➖➖➖➖➖➖➖➖➖➖➖➖\n',
                                    call.message.chat.id, call.message.message_id, reply_markup=kb)
    elif call.data == 'cancel_order':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data.startswith('check_lolzbuy_'): #check_lolzbuy_{rubles}_{com}_{num_check}_{user_id}
        amount = call.data.split('_')[2]
        comment = call.data.split('_')[3]
        number_check = call.data.split('_')[4]
        user_id = call.data.split('_')[5]
        tips = call.data.split('_')[6]
        print(amount)
        print(comment)
        result = await CheckPayment(market, amount=amount,comment=comment, include_payment_data=True)
        print(result)
        print("Status: " + str(result.status))
        print("Status code: " + str(result.status_code))
        print("Message: " + str(result.message))
        print("Payment data: " + str(result.payment_data))
        print("Parameters: " + str(result.parameters))
        if str(result.status_code) == '1':
            await bot.edit_message_text(f'Оплата прошла успешно. Идёт отправка...',
                                        call.message.chat.id, call.message.message_id)
            print(call.from_user.id)
            # async with db.DatabaseBot("Database/db.db") as db_bot:
            #    await db_bot.update_balance_user_plus(call.message.chat.id)
            async with db.DatabaseBot("Database/db.db") as db_bot:
                items = await db_bot.get_item(call.message.chat.id)

            # Assuming `items` is a list of tuples containing strings

            '''if isinstance(items, list):
                accounts = json.dumps(items)
            cleaned_string = accounts.strip("[]'")

            # Replace new line characters and unwanted separators
            cleaned_string = cleaned_string.replace("\\n", "\n").replace("', '", "\n")

            # Strip whitespace from each line and remove empty lines
            cleaned_string = "\n".join([line.strip() for line in cleaned_string.splitlines() if line.strip()])
'''
            strc = ""
            for idx, item in enumerate(items):
                it = item[0]
                cleaned_string = it.strip("[]'")
                cleaned_string = cleaned_string.replace("\\n", "\n").replace("', '", "\n")
                cleanedd_string = "\n".join([line.strip() for line in cleaned_string.splitlines() if line.strip()])
                print(cleanedd_string)

                cleanedt_text = cleanedd_string.strip('"')

                # Replace comma and space with a newline character
                cleaneds_text = cleanedt_text.replace('", "', '\n')
                rand = random.randint(1, 999999999999999)
                lines = cleaneds_text.split('\n')
                t = 0
                for value in lines:
                    print(lines[t])
                    parts = lines[t]
                    tt = parts.split(':')
                    geo = tt[0]
                    user = tt[1]
                    pass_tt = tt[2]
                    mail = tt[3]
                    pass_mail = tt[4]
                    text_file = ""
                    if tips == '1':
                        text_file = f"{mail}:{pass_mail}\n"
                    elif tips == '2':
                        text_file = f"@{user}:{pass_tt}\n"
                        print(f"tt{text_file}")
                    elif tips == '3':
                        text_file = f"@{user}:{pass_tt}:{mail}:{pass_mail}\n"
                    elif tips == '4':
                        text_file = f"{geo}:@{user}:{pass_tt}:{mail}:{pass_mail}\n"
                    print(text_file)
                    print(f'{t}+{lines[t]}')
                    file_path = f"Temp/giveacc/zakaz_{call.message.chat.id}_{rand}_{idx}.txt"
                    with open(file_path, "a") as file:
                        file.write(text_file)
                    t += 1

                await bot.send_document(call.message.chat.id,
                                        open(f'Temp/giveacc/zakaz_{call.message.chat.id}_{rand}_{idx}.txt', 'rb'))
                strc += cleaned_string
                os.remove(f'Temp/giveacc/zakaz_{call.message.chat.id}_{rand}_{idx}.txt')

            async with db.DatabaseBot("Database/db.db") as db_bot:
                itemss = await db_bot.sum_count_acc(call.message.chat.id)
            async with db.DatabaseBot("Database/db.db") as db_bot:
                res = await db_bot.get_user_bal(call.from_user.id)
            finall_count = int(itemss) + int(res)
            async with db.DatabaseBot("Database/db.db") as db_bot:
                await db_bot.update_balance_user(call.message.chat.id, finall_count)
            async with db.DatabaseBot("Database/db.db") as db_bot:
                await db_bot.insert_check(float(amount), number_check, user_id, strc)
            async with db.DatabaseBot("Database/db.db") as db_bot:
                await db_bot.delete_item(user_id)

        elif str(result.status_code) == '0':
            print(0)
            await call.answer(text="!!! Оплата не прошла !!!", show_alert=True)

    elif call.data == 'adm_stat':
        async with db.DatabaseBot("DataBase/db.db") as db_bot:
            count_user = await db_bot.get_counts_user()
        async with db.DatabaseBot("DataBase/db.db") as db_bot:
            sum_24_hours = await db_bot.sum_last_24_hours()
            sum_week = await db_bot.sum_last_week()
            sum_month = await db_bot.sum_last_month()
        await bot.edit_message_text(f'Кол-во пользователей в боте: {count_user}\n'
                                    f'\nПрибыль:\n\n'
                                    f'за 24 часа: {sum_24_hours} ₽\n'
                                    f'за неделю: {sum_week} ₽\n'
                                    f'за месяц: {sum_month} ₽\n',
                                    call.message.chat.id, call.message.message_id, reply_markup=adm_kb.cancel_adm_give_sum)


    elif call.data.startswith('outtxt'):
        await bot.edit_message_text('Введите гео аккаунтов которого желаете выгрузить', call.message.chat.id, call.message.message_id,
                                    reply_markup=adm_kb.cancel_adm_kb)
        await states.adm_states.input_del_acc_sum.set()

    elif call.data.startswith('concretgeoacc'):
        await bot.edit_message_text('Введите гео аккаунтов которое желаете удалить', call.message.chat.id, call.message.message_id,
                                    reply_markup=adm_kb.cancel_adm_kb)
        await states.adm_states.input_del_acc.set()

    elif call.data.startswith('menudeleteacc'):
        await bot.edit_message_text('Меню удаления', call.message.chat.id, call.message.message_id,
                                    reply_markup=adm_kb.menu_delete_acc)

    elif call.data.startswith('yes_or_no'):
        await bot.edit_message_text('Вы уверены?', call.message.chat.id, call.message.message_id,
                                    reply_markup=adm_kb.yes_or_no_acc_del)

    elif call.data.startswith('yes'):
        async with db.DatabaseBot("Database/db.db") as db_bot:
            await db_bot.delete_all_accs()
        await bot.edit_message_text('✔ Успешно удалено', call.message.chat.id, call.message.message_id)
        time.sleep(3)
        await bot.edit_message_text('Меню удаления', call.message.chat.id, call.message.message_id,
                                    reply_markup=adm_kb.menu_delete_acc)

    elif call.data.startswith('prcheck_pay_'):
        try:
            id_pay = call.data.split('_')[2]
            amount = call.data.split('_')[3]
            status = await cryptobot.check_status(amount,id_pay)
            if status == 'paid':
                await bot.edit_message_text(f'Оплата прошла успешно, деньги зачислены на баланс ✔',
                                            call.message.chat.id, call.message.message_id, reply_markup=user_kb.main_menu)
                async with db.DatabaseBot("Database/db.db") as db_bot:
                    res = await db_bot.get_user_bal(call.from_user.id)
                mon = int(res) + int(amount)
                print(mon)
                print(call.from_user.id)
                async with db.DatabaseBot("Database/db.db") as db_bot:
                    await db_bot.update_balance_user(call.message.chat.id, mon)
                async with db.DatabaseBot("Database/db.db") as db_bot:
                    await db_bot.insert_purchase(int(amount))
        except Exception as e:
            print(traceback.format_exc())

    elif call.data.startswith('prcheck_buy_'): #prcheck_buy_{rez_pay[1]}_{sum}_{number_check}_{user_id}
        try:
            id_pay = call.data.split('_')[2]
            amount = call.data.split('_')[3]
            number_check = call.data.split('_')[4]
            user_id = call.data.split('_')[5]
            tips = call.data.split('_')[6]

            status = await cryptobot.check_status(amount,id_pay)
            if status == 'paid':
                await bot.edit_message_text(f'Оплата прошла успешно. Идёт отправка...',
                                            call.message.chat.id, call.message.message_id)
                print(call.from_user.id)
                #async with db.DatabaseBot("Database/db.db") as db_bot:
                #    await db_bot.update_balance_user_plus(call.message.chat.id)
                async with db.DatabaseBot("Database/db.db") as db_bot:
                    items = await db_bot.get_item(call.message.chat.id)

                # Assuming `items` is a list of tuples containing strings


                '''if isinstance(items, list):
                    accounts = json.dumps(items)
                cleaned_string = accounts.strip("[]'")

                # Replace new line characters and unwanted separators
                cleaned_string = cleaned_string.replace("\\n", "\n").replace("', '", "\n")

                # Strip whitespace from each line and remove empty lines
                cleaned_string = "\n".join([line.strip() for line in cleaned_string.splitlines() if line.strip()])
'''
                strc = ""
                for idx, item in enumerate(items):
                    it = item[0]
                    cleaned_string = it.strip("[]'")
                    cleaned_string = cleaned_string.replace("\\n", "\n").replace("', '", "\n")
                    cleanedd_string = "\n".join([line.strip() for line in cleaned_string.splitlines() if line.strip()])
                    print(cleanedd_string)

                    cleanedt_text = cleanedd_string.strip('"')

                    # Replace comma and space with a newline character
                    cleaneds_text = cleanedt_text.replace('", "', '\n')
                    rand = random.randint(1, 999999999999999)
                    lines = cleaneds_text.split('\n')
                    t = 0
                    for value in lines:
                        print(lines[t])
                        parts = lines[t]
                        tt = parts.split(':')
                        geo = tt[0]
                        user = tt[1]
                        pass_tt = tt[2]
                        mail = tt[3]
                        pass_mail = tt[4]
                        text_file = ""
                        if tips == '1':
                            text_file = f"{mail}:{pass_mail}\n"
                        elif tips == '2':
                            text_file = f"@{user}:{pass_tt}\n"
                            print(f"tt{text_file}")
                        elif tips == '3':
                            text_file = f"@{user}:{pass_tt}:{mail}:{pass_mail}\n"
                        elif tips == '4':
                            text_file = f"{geo}:@{user}:{pass_tt}:{mail}:{pass_mail}\n"
                        print(text_file)
                        print(f'{t}+{lines[t]}')
                        file_path = f"Temp/giveacc/out_{call.message.chat.id}_{rand}_{idx}.txt"
                        with open(file_path, "a") as file:
                            file.write(text_file)
                        t += 1
                    # Get the third line (index 2)
                    third_line = lines[2]

                    # Print the third line
                    print(third_line)

                    # Print the result
                    print(cleaneds_text)


                    await bot.send_document(call.message.chat.id, open(f'Temp/giveacc/out_{call.message.chat.id}_{rand}_{idx}.txt', 'rb'))
                    strc += cleaned_string
                    os.remove(f'Temp/giveacc/out_{call.message.chat.id}_{rand}_{idx}.txt')

                async with db.DatabaseBot("Database/db.db") as db_bot:
                    itemss = await db_bot.sum_count_acc(call.message.chat.id)
                async with db.DatabaseBot("Database/db.db") as db_bot:
                    res = await db_bot.get_user_bal(call.from_user.id)
                finall_count = int(itemss) + int(res)
                async with db.DatabaseBot("Database/db.db") as db_bot:
                    await db_bot.update_balance_user(call.message.chat.id, finall_count)
                async with db.DatabaseBot("Database/db.db") as db_bot:
                    await db_bot.insert_check(float(amount), number_check, user_id, strc)
                async with db.DatabaseBot("Database/db.db") as db_bot:
                    await db_bot.delete_item(user_id)

        except Exception as e:
            print(traceback.format_exc())

            '''elif call.data == 'format_':
        total_amount = call.data.split('_')[1]
        number_check = call.data.split('_')[2]
        user_id = call.data.split('_')[3] '''



    elif call.data.startswith('profile_pay_'):
        type_crypto = call.data.split('_')[2]
        sum = call.data.split('_')[3]
        rez_pay = await cryptobot.order(int(sum), type_crypto)
        kb = InlineKeyboardMarkup(row_width=1)
        q = InlineKeyboardButton(text='Перейти к оплате', url=rez_pay[0])
        qq = InlineKeyboardButton(text='Проверить оплату', callback_data=f'prcheck_pay_{rez_pay[1]}_{sum}')
        w = InlineKeyboardButton(text='Отменить', callback_data=f'prof_cancel_order')
        kb.add(q, qq, w)
        await bot.edit_message_text(f'🆙 Пополнение\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n💰 Сумма пополнения: {sum} ₽ \n➖➖➖➖➖➖➖➖➖➖➖➖➖\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ‼️После оплаты, обязательно нажмите проверить оплату‼️ ',
                                    call.message.chat.id, call.message.message_id, reply_markup=kb)

    elif call.data.startswith('profile_buy_'):
        type_crypto = call.data.split('_')[2]
        sum = call.data.split('_')[3]
        print(float(sum))
        number_check = call.data.split('_')[4]
        user_id = call.data.split('_')[5]
        tips = call.data.split('_')[6]
        rez_pay = await cryptobot.order(float(sum), type_crypto)
        kb = InlineKeyboardMarkup(row_width=1)
        q = InlineKeyboardButton(text='Перейти к оплате', url=rez_pay[0])
        qq = InlineKeyboardButton(text='Проверить оплату', callback_data=f'prcheck_buy_{rez_pay[1]}_{sum}_{number_check}_{user_id}_{tips}')
        w = InlineKeyboardButton(text='Отменить', callback_data=f'prof_cancel_order')
        kb.add(q, qq, w)
        await bot.edit_message_text(f'🆙 Пополнение\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n💰 Сумма пополнения: {sum} ₽ \n➖➖➖➖➖➖➖➖➖➖➖➖➖\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ‼️После оплаты, обязательно нажмите проверить оплату‼️',
                                    call.message.chat.id, call.message.message_id, reply_markup=kb)

    elif call.data.startswith('tipbuy_'):
        amount = call.data.split('_')[1]
        number_check = call.data.split('_')[2]
        user_id = call.data.split('_')[3]
        tips = call.data.split('_')[4]
        com = random.randint(1000000000000,999999999999999999999)
        print(1)
        await bot.edit_message_text('Выберите способ оплаты', call.message.chat.id, call.message.message_id,
                                    reply_markup=await user_kb.profile_buyments_kb(amount, com, number_check, user_id, tips))


    elif call.data == 'prof_cancel_order':
        await bot.edit_message_text(
            f'Отмена оплаты',
            call.message.chat.id, call.message.message_id)

    elif call.data.startswith('for_'):
        format = call.data.split('_')[1]
        amount = call.data.split('_')[2]
        number_check = call.data.split('_')[3]
        user_id = call.data.split('_')[4]
        com = random_string(30)
        print(1)
        print(1)
        #await bot.edit_message_text('Выберите способ оплаты', call.message.chat.id, call.message.message_id, reply_markup=await user_kb.profile_buyments_kb(amount, com, number_check, user_id))
        print(call.message.chat.id)
        async with db.DatabaseBot("Database/db.db") as db_bot:
            id_cart = await db_bot.get_id_cart(call.message.chat.id)
        async with db.DatabaseBot("Database/db.db") as db_bot:
            items = await db_bot.get_items(call.message.chat.id)
        print(f"{items}\n↑ items")
        total_amount = 0.0
        for item in items:
            id_value, country, amount = item
            total_amount += amount
        if format == '1':
            text_message = 'mail:pass_mail'
        elif format == '2':
            text_message = '@user:pass_TT'
        elif format == '3':
            text_message = '@user:pass_TT:mail:pass_mail'
        elif format == '4':
            text_message = 'GEO:@user:pass_TT:mail:pass_mail'
        response_text = ""
        if items:
            total_amount = 0
            number_check = str(id_cart[0][0])
            user_id = call.message.chat.id
            response_text = (f"Номер вашего заказа: <code>{str(id_cart[0][0])}</code>\n\n"
                             f"Ваша корзина:\n")
            for item in items:
                id_value, country, amount = item
                # print(f"Обработанный элемент: Количество={id_value}, Страна={country}, Сумма={amount}, Текущая общая сумма={total_amount}")
                response_text += (f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                  f"Страна {country} | {id_value} шт | {amount} ₽\n"
                                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n")
                total_amount += amount

            response_text += (f"Сумма к оплате: {total_amount} ₽\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                              f"Выбран формат:\n"
                              f"*️⃣ {text_message}")
            await bot.edit_message_text(response_text,chat_id=call.message.chat.id, message_id=call.message.message_id,#parse_mode='Markdown',
                                 reply_markup=await user_kb.cart_less_pay(total_amount, number_check, user_id, format))
        else:
            await bot.send_message(call.message.chat.id, "🛒 Корзина пуста", reply_markup=user_kb.kb_cart_shop)


    elif call.data.startswith('bkt_'):
        amount = call.data.split('_')[1]
        number_check = call.data.split('_')[2]
        user_id = call.data.split('_')[3]
        com = random_string(30)
        print(1)
        print(2)
        #await bot.edit_message_text('Выберите способ оплаты', call.message.chat.id, call.message.message_id, reply_markup=await user_kb.profile_buyments_kb(amount, com, number_check, user_id))
        print(call.message.chat.id)
        async with db.DatabaseBot("Database/db.db") as db_bot:
            id_cart = await db_bot.get_id_cart(call.message.chat.id)
        async with db.DatabaseBot("Database/db.db") as db_bot:
            items = await db_bot.get_items(call.message.chat.id)
        print(f"{items}\n↑ items")
        total_amount = 0.0
        # Итерация по каждому кортежу
        for item in items:
            id_value, country, amount = item
            # Сложение amount
            total_amount += amount

        # Печать суммы всех amount
        response_text = ""
        if items:
            total_amount = 0
            # Извлечение значения
            number_check = str(id_cart[0][0])
            user_id = call.message.chat.id
            response_text = (f"Номер вашего заказа: <code>{str(id_cart[0][0])}</code>\n\n"
                             f"Ваша корзина:\n")
            for item in items:
                id_value, country, amount = item
                # print(f"Обработанный элемент: Количество={id_value}, Страна={country}, Сумма={amount}, Текущая общая сумма={total_amount}")
                response_text += (f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                  f"Страна {country} | {id_value} шт. | {amount} ₽\n"
                                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n")
                total_amount += amount

            response_text += (f"Сумма к оплате: {total_amount} ₽\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                              f"🧾 Выберите формат:\n\n"
                              f"1️⃣ - mail:pass_mail\n"
                              f"2️⃣ - @user:pass_TT\n"
                              f"3️⃣ - @user:pass_TT:mail:pass_mail\n"
                              f"4️⃣ - GEO:@user:pass_TT:mail:pass_mail\n")
            await bot.edit_message_text(response_text,chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 reply_markup=await user_kb.cart_less_format(total_amount, number_check, user_id))
        else:
            await bot.send_message(call.message.chat.id, "🛒 Корзина пуста", reply_markup=user_kb.kb_cart_shop)

    '''elif call.data.startswith( 'additemin'):
        #await bot.edit_message_text('Введите кол-во аккаунтов',call.message.chat.id,call.message.message_id,reply_markup=user_kb.kb_shop_back)
        data = await state.get_data()
        tips = data["tipst"]
        geo = data["geo"]
        count = data["count"]
        await state.finish()
        geo = call.data.split('_')[2]
        print(geo)
        count = call.data.split('_')[3]
        print(count)
        tips = call.data.split('_')[4]
        print(tips)

        async with db.DatabaseBot("Database/db.db") as db_bot:
            accounts = await db_bot.get_select_geo_by_tips(geo,tips)
            print(accounts)

        await bot.send_message(call.message.chat.id, f"Успешно добавлен в вашу корзину. ✔",
                               )'''

    '''await states.user_states.new_acc_buy.set()
                state = Dispatcher.get_current().current_state()
                await state.update_data(geo=geo)
                await state.update_data(price=price)
                await state.update_data(count=count)'''
    '''result = extract_lines(geo, count)
        print(result)'''
     #   async with db.DatabaseBot("Database/db.db") as db_bot:
              #  await db_bot.add_item(call.message.chat.id, geo, str(result), price, count)

    '''async with db.DatabaseBot("Database/db.db") as db_bot:
            await db_bot.add_cart_acc(geo, price, count)
        '''

@dp.message_handler(state = states.adm_states.mailing)
async def adm_states_mailing(message:types.Message,state = FSMContext):
    text = message.text
    await state.finish()
    if text.isalpha():
        async with db.DatabaseBot("DataBase/db.db") as db_bot:
            all_users = await db_bot.get_all_users()
        for user in all_users:
            try:
                await bot.send_message(user[1],text = text)
            except:
                pass
        await bot.send_message(message.chat.id,text = 'Рассылка завершена 💌')
        await bot.send_message(message.chat.id,text = 'Админ панель',reply_markup=adm_kb.adm_menu)
@dp.callback_query_handler(state=states.adm_states.mailing)
async def adm_states_mailing(call: CallbackQuery, state=FSMContext):
    await state.finish()
    await bot.edit_message_text('Админ панель', call.message.chat.id, call.message.message_id,
                                reply_markup=adm_kb.adm_menu)


@dp.message_handler(state=states.user_states.new_acc_buy)
async def user_states_new_acc_buy(message: types.Message, state: FSMContext):
    countuser = message.text
    if countuser.isdigit():
        data = await state.get_data()
        tips = data["tipst"]
        geo = data["geo"]
        price = data["price"]
        message_i = data["message_id"]
        if tips == '1':
            otlega = 'меньше 4ч'
        elif tips == '2':
            otlega = 'больше 4ч'
        elif tips == '3':
            otlega = 'больше 12ч'
        elif tips == '4':
            otlega = 'больше 24ч'
        elif tips == '5':
            otlega = 'больше 36ч'
        async with db.DatabaseBot("Database/db.db") as db_bot:
            count = await db_bot.get_count_geo(geo)
        response_message = (
            f"Регион: {geo}\nОтлежка: {otlega}\n\n"
            f"⬇️Укажите количество аккаунтов сообщением⬇️\n"
            f"(просто отправьте цифру в чат)!\n\n"
            f"<u>Если Вы ошиблись, цифру можно ввести повторно🔄</u>\n\n"
            f"✅ Доступно к покупке: {count} шт.\n\n"
            f"🛒 Количество: {int(countuser)} шт."
        )
        await bot.edit_message_text(text=response_message,chat_id=message.chat.id, message_id=message_i, reply_markup=await user_kb.write_cart(geo, int(countuser), int(tips), price))
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await states.user_states.new_acc_buy.set()
        state = Dispatcher.get_current().current_state()
        await state.update_data(geo=geo)
        await state.update_data(tipst=tips)
        await state.update_data(count=countuser)

@dp.callback_query_handler(state=states.user_states.new_acc_buy)
async def user_states_new_acc_buy(call: CallbackQuery, state: FSMContext):
        if call.data.startswith('backaccbuy_'):
            geo = call.data.split('_')[1]
            price = call.data.split('_')[2]
            async with db.DatabaseBot("Database/db.db") as db_bot:
                counts = await db_bot.get__geo(geo)
            message = (
                f"Регион: {geo}\n ⬇️⬇️Доступно к покупке⬇️⬇️\n \n"
                f"1️⃣ - Отлежка меньше 4ч: {counts['less_4h']} шт.\n\n"
                f"2️⃣ - Отлежка больше 4ч: {counts['more_4h_less_12h']} шт.\n\n"
                f"3️⃣ - Отлежка больше 12ч: {counts['more_12h_less_24h']} шт.\n\n"
                f"4️⃣ - Отлежка больше 24ч: {counts['more_24h_less_36h']} шт.\n\n"
                f"5️⃣ - Отлежка больше 36ч: {counts['more_36h']} шт."
            )
            c1 = int(counts['less_4h'])
            c2 = int(counts['more_4h_less_12h'])
            c3 = int(counts['more_12h_less_24h'])
            c4 = int(counts['more_24h_less_36h'])
            c5 = int(counts['more_36h'])
            await bot.edit_message_text(message, call.message.chat.id, call.message.message_id,
                                        reply_markup=await user_kb.time_otlega(geo, price, c1, c2, c3, c4, c5))
        elif call.data.startswith('showshopp'):
            await bot.edit_message_text(f"---------------- В наличии ----------------\n", call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=await user_kb.shop_menu_acc())

        elif call.data == 'cartback':
            print(call.message.from_user.id)
            async with db.DatabaseBot("Database/db.db") as db_bot:
                id_cart = await db_bot.get_id_cart(call.message.chat.id)
            async with db.DatabaseBot("Database/db.db") as db_bot:
                items = await db_bot.get_items(call.message.chat.id)
            print(f"{items}\n↑ items")
            total_amount = 0.0
            for item in items:
                id_value, country, amount = item
                total_amount += amount

            response_text = ""
            if items:
                total_amount = 0
                # Извлечение значения
                number_check = str(id_cart[0][0])
                user_id = call.message.chat.id
                response_text = (f"Номер вашего заказа: `{str(id_cart[0][0])}`\n\n"
                                 f"Ваша корзина:\n")
                for item in items:
                    id_value, country, amount = item
                    # print(f"Обработанный элемент: Количество={id_value}, Страна={country}, Сумма={amount}, Текущая общая сумма={total_amount}")
                    response_text += (f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"Страна {country} | {id_value} шт. | {amount} ₽\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n")
                    total_amount += amount

                response_text += f"\nСумма к оплате: {total_amount} ₽ "

                await call.message.answer(response_text, parse_mode='Markdown',
                                     reply_markup=await user_kb.cart_pay(total_amount, number_check, user_id))
            else:
                await bot.send_message(call.message.chat.id, "🛒 Корзина пуста", reply_markup=user_kb.kb_cart_shop)


        elif call.data.startswith('additemin_'):
            data = await state.get_data()
            tips = data["tipst"]
            geo = data["geo"]
            count = data["count"]
            await state.finish()
            print(geo, count, tips)
            async with db.DatabaseBot("Database/db.db") as db_bot:
                if tips == '1':
                    accounts = await db_bot.get_acc_less_than_4_hours(count, geo)
                elif tips == '2':
                    accounts = await db_bot.get_acc_between_4_and_12_hours(count, geo)
                elif tips == '3':
                    accounts = await db_bot.get_acc_min_24_max12(count, geo)
                elif tips == '4':
                    accounts = await db_bot.get_acc_between_24_and_36_hours(count, geo)
                elif tips == '5':
                    accounts = await db_bot.get_acc_greater_than_36_hours(count, geo)
                account = accounts
                price = await db_bot.get_price_country(geo)
                print(price[0])
                price_fin = int(count) * int(price[0])
                print(call.message.chat.id, geo, accounts, count, price_fin)

                async with db.DatabaseBot("Database/db.db") as db_bot:
                    if isinstance(accounts, list):
                        accounts = json.dumps(accounts)
                    await db_bot.add_item(call.message.chat.id, geo, accounts, price_fin, count)
                for entry in account:
                    print("Удалён → " + entry)
                    async with db.DatabaseBot("Database/db.db") as db_bot:
                        await db_bot.delete_item_item(entry)
            await bot.edit_message_text(f"Успешно добавлен в вашу корзину. ✔\n"
                                        f"❗ Через 30 минут, ваша корзина будет очищена", call.message.chat.id,
                                        call.message.message_id)
    #    state = Dispatcher.get_current().current_state()

'''count = message.text
    data = await state.get_data()
    await state.finish()
    dt = data["price"]
    country_count = {}
    with open('accounts.txt', 'r') as file:
        for line in file:
            if line.strip():  # Проверяем, что строка не
                # пустая
                country_code = line.split(':')[0]
                if country_code in country_count:
                    country_count[country_code] += 1
                else:
                    country_count[country_code] = 1
    count_accs = country_count[data["geo"]]
    if int(count_accs) < int(count):
        await bot.send_message(message.chat.id, text ='Недостаточно аккаунтов', reply_markup=await user_kb.get_accs())
    else:
        await bot.send_message(message.chat.id, text=f'Регион: {data["geo"]}\n'
                                                     f'Кол-во аккаунтов: {count}\n'
                                                     f'Цена: {int(count)*float(dt)} ₽',
                               reply_markup=await user_kb.shop_acc_kb(data["geo"], int(count)*float(dt), count))'''


@dp.message_handler(state=states.user_states.new_balance)
async def user_states_new_balance(message: types.Message, state=FSMContext):
    amount = message.text
    com = random.randint(10000000,100000000000000)
    ran = f"{com}_{random_string(30)}"
    await state.finish()
    await bot.send_message(message.chat.id, text='Выберите чем желаете пополнить', reply_markup= await user_kb.profile_payments_kb(amount, ran))


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=states.adm_states.get_shop_acc)
async def handle_docs(message: types.Message, state: FSMContext):
    document = message.document
    if document.mime_type == 'text/plain':
        file_info = await bot.get_file(document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        file_content = downloaded_file.read().decode('utf-8')
        lines = file_content.splitlines()
        non_empty_lines = [line for line in lines if line.strip() != ""]
        filtered_content = "\n".join(non_empty_lines)
        for line in non_empty_lines:
            print(line)
            geo_acc = line.split(':')[0]
            print(geo_acc)
            async with db.DatabaseBot("DataBase/db.db") as db_bot:
                await db_bot.insert_account(geo_acc, line)
            print('Добавили в бд')


        file_path = f'temp_{document.file_name}'
        with open(file_path, 'wb') as temp_file:
            temp_file.write(downloaded_file.getvalue())
        os.remove(file_path)
        await message.reply("Файл обработан и его содержимое добавлено в БД")
        await state.finish()
    else:
        await message.reply("Пожалуйста, пришлите текстовый файл (формат .txt).")


@dp.message_handler(state=states.adm_states.input_new_geo_sum_for_edit)
async def adm_states_input_geo_sum(message:types.Message,state = FSMContext):
    input_geo_sums = message.text
    await state.update_data(sub_id=input_geo_sums)
    await bot.send_message(message.chat.id, text='Введите цену в ₽', reply_markup=adm_kb.adm_menu_geo_back)
    await states.adm_states.new_input_new_geo_sum_edit.set()

@dp.message_handler(state=states.adm_states.new_input_new_geo_sum_edit)
async def adm_states_new_input_new_geo_sum(message: types.Message, state: FSMContext):
    money = message.text
    data = await state.get_data()
    await state.finish()
    sum_id = data['sub_id']
    async with db.DatabaseBot("DataBase/db.db") as db_bot:
        user_info = await db_bot.get_countries_sum(str(sum_id))
    print(str(user_info[1]), str(sum_id))
    print(float(money))
    if str(user_info[1]) == str(sum_id):
        async with db.DatabaseBot("DataBase/db.db") as db_bot:
            await db_bot.update_geo_acc(sum_id, float(money))
        # await db_bot.commit()
        await bot.send_message(message.chat.id, text='Стоимость обновлена.\n')
    else:
        await bot.send_message(message.chat.id, text='Стоимость не была обновлена. Ошибка\n')
    await bot.send_message(message.chat.id, text='Админ панель', reply_markup=adm_kb.adm_menu)


@dp.message_handler(state=states.adm_states.new_input_new_geo_sum)
async def adm_states_new_input_new_geo_sum(message: types.Message, state: FSMContext):
    money = message.text
    data = await state.get_data()
    await state.finish()
    geo = data['sub_id']
    name = data['sub']
    async with db.DatabaseBot("Database/db.db") as db_bot:
        await db_bot.add_geo_acc(geo, name, float(money))
        # await db_bot.commit()
    await bot.send_message(message.chat.id, text='Гео добавлено\n')
    await bot.send_message(message.chat.id, text='Админ панель', reply_markup=adm_kb.adm_menu)
    '''money = message.text
    data = await state.get_data()
    await state.finish()
    sum_id = data['sub_id']
    async with db.DatabaseBot("Database/db.db") as db_bot:
        await db_bot.add_geo_acc(sum_id, float(money))
           # await db_bot.commit()
    await bot.send_message(message.chat.id, text='Гео добавлено\n')
    await bot.send_message(message.chat.id, text='Админ панель', reply_markup=adm_kb.adm_menu)
    '''


@dp.message_handler(state=states.adm_states.input_del_acc)
async def adm_states_input_acc_sum(message:types.Message,state = FSMContext):
    input_geo_sums_new = message.text
    await state.finish()
    print(input_geo_sums_new)
    async with db.DatabaseBot("Database/db.db") as db_bot:
        await db_bot.delete_concret_accs(str(input_geo_sums_new))
    await bot.send_message(text='✔ Успешно удалено', chat_id=message.chat.id)
    time.sleep(3)
    await bot.send_message(text='Меню удаления', chat_id=message.chat.id,
                                reply_markup=adm_kb.menu_delete_acc)


@dp.message_handler(state=states.adm_states.input_del_acc_sum)
async def adm_states_input_acc_sum(message:types.Message,state=FSMContext):
    input_geo_sums_new = message.text
    await state.finish()
    print(input_geo_sums_new)
    async with db.DatabaseBot("Database/db.db") as db_bot:
        ass = await db_bot.get_accounts_from(str(input_geo_sums_new))
    print(52)
    print(ass)
    print(ass)
    for value in ass:
        print(value[0])
        parts = value
        file_path = f"Temp/giveacc/accaunt_vygruzka_{input_geo_sums_new}.txt"
        with open(file_path, "a") as file:
            file.write(f'{value[0]}\n')
    await bot.send_document(message.chat.id,
                            open(f'Temp/giveacc/accaunt_vygruzka_{input_geo_sums_new}.txt', 'rb'))
    os.remove(f'Temp/giveacc/accaunt_vygruzka_{input_geo_sums_new}.txt')

@dp.message_handler(state=states.adm_states.input_new_geo_sum)
async def adm_states_input_geo_sum(message:types.Message,state = FSMContext):
    input_geo_sums_new = message.text
    await state.finish()
    await state.update_data(sub_id=input_geo_sums_new)
    await bot.send_message(message.chat.id, text='Введите название для гео, можно использовать флаги стран', reply_markup=adm_kb.adm_menu_geo_back)
    await states.adm_states.input_new_geo_sum_new.set()

'''@dp.callback_query_handler(lambda c: c.data.startswith('additemin'), state=states.user_states.new_acc_buy)
async def handle_add_item(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tips = data["tipst"]
    geo = data["geo"]
    count = data["count"]
    await state.finish()
    print(geo, count, tips)
    async with db.DatabaseBot("Database/db.db") as db_bot:
        if tips == '1':
            accounts = await db_bot.get_acc_less_than_4_hours(count, geo)
        elif tips == '2':
            accounts = await db_bot.get_acc_between_4_and_12_hours(count, geo)
        elif tips == '3':
            accounts = await db_bot.get_acc_min_24_max12(count, geo)
        elif tips == '4':
            accounts = await db_bot.get_acc_between_24_and_36_hours(count, geo)
        elif tips == '5':
            accounts = await db_bot.get_acc_greater_than_36_hours(count, geo)
        account = accounts
        price = await db_bot.get_price_country(geo)
        print(price[0])
        price_fin = int(count) * int(price[0])
        print(call.message.chat.id, geo, accounts, count, price_fin)

        async with db.DatabaseBot("Database/db.db") as db_bot:
            if isinstance(accounts, list):
                accounts = json.dumps(accounts)
            await db_bot.add_item(call.message.chat.id, geo, accounts, price_fin, count)
        for entry in account:
            print("Удалён → "+ entry)
            async with db.DatabaseBot("Database/db.db") as db_bot:
                await db_bot.delete_item_item(entry)
    await bot.edit_message_text(f"Успешно добавлен в вашу корзину. ✔\n"
                                f"❗ Через 30 минут, ваша корзина будет очищена", call.message.chat.id,
                                call.message.message_id)
'''

@dp.message_handler(state=states.adm_states.input_new_geo_sum_new)
async def adm_states_input_geo_sum(message:types.Message,state = FSMContext):
    input_geo_sum = message.text
    await state.update_data(sub=input_geo_sum)
    await bot.send_message(message.chat.id, text='Введите цену в ₽', reply_markup=adm_kb.adm_menu_geo_back)
    await states.adm_states.new_input_new_geo_sum.set()


'''@dp.message_handler(state=states.adm_states.new_input_new_geo_sum)
async def adm_states_new_input_new_geo_sum(message: types.Message, state: FSMContext):
    money = message.text
    data = await state.get_data()
    await state.finish()
    geo = data['sub_id']
    name = data['sub']
    async with db.DatabaseBot("Database/db.db") as db_bot:
        await db_bot.add_geo_acc(geo,name, float(money))
           # await db_bot.commit()
    await bot.send_message(message.chat.id, text='Гео добавлено\n')
    await bot.send_message(message.chat.id, text='Админ панель', reply_markup=adm_kb.adm_menu)
'''
@dp.callback_query_handler(state=states.user_states.proxy)
async def user_states_accounts(call: CallbackQuery, state=FSMContext):
        await state.finish()
        if call.data == 'cancel_mail':
            await bot.edit_message_text('Введите id пользователя', call.message.chat.id, call.message.message_id,
                                        reply_markup=user_kb.main_menu)



@dp.message_handler(state = states.adm_states.get_sum_id)
async def adm_states_get_sum_id(message:types.Message,state = FSMContext):
    sum_user_id = message.text
    await state.update_data(sub_id=sum_user_id)
    await bot.send_message(message.chat.id, text='Введите сумму которую нужно добавить')
    await states.adm_states.new_give_money.set()


@dp.message_handler(state = states.adm_states.new_give_money)
async def adm_states_new_money_days(message:types.Message, state=FSMContext):
    money = message.text
    data = await state.get_data()
    await state.finish()
    sum_id = data['sub_id']
    async with db.DatabaseBot("Database/db.db") as db_bot:
        user_info = await db_bot.get_user_bal(sum_id)
    if user_info[4] == '0':
        async with db.DatabaseBot("Database/db.db") as db_bot:
            await db_bot.add_sum(sum_id, float(money))
    else:
        final_balance = float(user_info[4]) + float(money)
        async with db.DatabaseBot("Database/db.db") as db_bot:
            await db_bot.update_sum(sum_id,final_balance)
    await bot.send_message(message.chat.id, text ='Баланс обновлён.\n'
                                                  f'Новый баланс пользователя {sum_id}: {float(final_balance)}₽')
    await bot.send_message(message.chat.id, text ='Выберите нужные настройки', reply_markup=adm_kb.adm_menu)

    async with db.DatabaseBot("Database/db.db") as db_bot:
        await db_bot.delete_old_items()

@dp.message_handler(state=states.adm_states.input_del_geo_sum)
async def adm_states_input_geo_sum(message:types.Message, state = FSMContext):
    input_geo_sums = message.text
    await state.finish()
    async with db.DatabaseBot("DataBase/db.db") as db_bot:
        await db_bot.del_geo_acc(input_geo_sums)
    await bot.send_message(message.chat.id, text='Гео удалено\n')

'''async def delete_old_items_periodically():
    while True:
        await delete_old_items()
        await asyncio.sleep(60)  # Check every minute

async def on_startup(dp):
    await init_db()
    asyncio.create_task(delete_old_items_periodically())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)'''

async def on_startup(_):
    asyncio.create_task(delete_old_items_periodically())

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True, on_startup=on_startup)