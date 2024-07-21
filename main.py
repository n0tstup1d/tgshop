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
        async with db.DatabaseBot("DataBase/db.db") as db_bot:
            user_info = await db_bot.get_user_bal(message.chat.id)
        await bot.send_message(message.chat.id, f"Ваш ID: `{message.chat.id}`\n"
                                                f"\n"
                                                f"Ваш баланс: {user_info[4]}$\n"
                                                f"\n"
                                                f"Куплено аккаунтов: бд нет\n"
                                                f"Может сделать на все товары как написанно выше ", reply_markup=user_kb.main_menu, parse_mode='Markdown')
    if message.text == "🛒 Магазин":
        '''async with db.DatabaseBot("Database/bd.db") as db_bot:
            res = await db_bot.get_accont()'''
        await bot.send_message(message.chat.id, f"--------------- В наличии ---------------\n",
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
    '''if message.text == "💌 Получить код с почты":
        await bot.send_message(message.chat.id,"Введите вашу почту", reply_markup=await user_kb.mail_back_kb())
        await states.user_states.for_maill.set()'''

    if message.text == '🖤 Меню подписки':
        async with db.DatabaseBot("Database/db.db") as db_bot:
            rez = await db_bot.check_users_sub(message.from_user.id)
            print(rez)
        today = datetime.today()
        formatted_date = today.strftime('%Y-%m-%d')
        if rez < formatted_date:
            await bot.send_message(message.chat.id,
                                                "__У вас отсутвует подписка__ 😕\n"
                                                "\n"
                                                "При покупки подписки вы получаете:\n\n"
                                                "♦ Тик Ток Чекер 🖤\n"
                                                "♦ Получение кодов от почты 💌\n"
                                                "♦ Уникализатор видео и фото 🖼",  parse_mode=ParseMode.MARKDOWN_V2 ,reply_markup=await user_kb.mail_back_kb())
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
        with open('accounts.txt', 'r') as file:
            lines = file.readlines()
        region_counts = {}
        for line in lines:
            region = line.split(':')[0]
            if region in region_counts:
                region_counts[region] += 1
            else:
                region_counts[region] = 1
        for region, count in region_counts.items():
            print(f"{region} | {count}")
            message += f"{region} | {count}\n"
        await bot.edit_message_text(message,call.message.chat.id, call.message.message_id,
                                    reply_markup=adm_kb.adm_menu_acc_shop)
    elif call.data == 'SettingsGeo':
        async with db.DatabaseBot("DataBase/db.db") as db_bot:
            countries = await db_bot.get_countries_acc()
        message = "Список регионов и их цены:\n"
        if countries:
            for region, price in countries:
                message += f"{region}: {price}\n"
            await bot.edit_message_text(message, call.message.chat.id, call.message.message_id,
                                        reply_markup=adm_kb.adm_add_geo)
        else:
            await bot.edit_message_text('Тут должен быть список гео, но пока гео нет(', call.message.chat.id, call.message.message_id,
                                        reply_markup=adm_kb.adm_add_geo)
    elif call.data == 'addnewGEO':
        async with db.DatabaseBot("DataBase/db.db") as db_bot:
            countries = await db_bot.get_countries_acc()
        if countries:
            message = ('Введите новое гео капсом:\n'
                       'Существующие:\n')
            for country in countries:
                message += f'Название: {country[1]}, Цена: {country[2]}\n'
        else:
            message = 'В базе данных нет информации о странах.'
        await bot.edit_message_text(message,call.message.chat.id,call.message.message_id,reply_markup=adm_kb.adm_menu_geo_back)
        await states.adm_states.input_new_geo_sum.set()

    elif call.data == 'menuaddaccshop':
        await bot.edit_message_text('Скиньте файл ( .txt ) с аккаунтами (можно с разными гео)', call.message.chat.id, call.message.message_id,
                                    reply_markup=adm_kb.cancel_adm_acc_add)
        await states.adm_states.get_shop_acc.set()

    elif call.data.startswith('AccBuy_'):
        await bot.edit_message_text('Введите кол-во аккаунтов',call.message.chat.id,call.message.message_id,reply_markup=adm_kb.cancel_adm_kb)
        geo = call.data.split('_')[1]
        price = call.data.split('_')[2]
        await states.user_states.new_acc_buy.set()
        state = Dispatcher.get_current().current_state()
        await state.update_data(geo=geo)
        await state.update_data(price=price)


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
        with open('accounts.txt', 'a') as accounts_file:
            accounts_file.write(filtered_content + '\n')
        file_path = f'temp_{document.file_name}'
        with open(file_path, 'wb') as temp_file:
            temp_file.write(downloaded_file.getvalue())
        os.remove(file_path)
        await message.reply("Файл обработан и его содержимое добавлено в accounts.txt.")
        await state.finish()
    else:
        await message.reply("Пожалуйста, пришлите текстовый файл (формат .txt).")


@dp.message_handler(state=states.adm_states.input_new_geo_sum)
async def adm_states_input_geo_sum(message:types.Message,state = FSMContext):
    input_geo_sums = message.text
    await state.update_data(sub_id=input_geo_sums)
    await bot.send_message(message.chat.id, text='Введите цену в $', reply_markup=adm_kb.adm_menu_geo_back)
    await states.adm_states.new_input_new_geo_sum.set()

@dp.message_handler(state=states.adm_states.new_input_new_geo_sum)
async def adm_states_new_input_new_geo_sum(message: types.Message, state: FSMContext):
    money = message.text
    data = await state.get_data()
    await state.finish()
    sum_id = data['sub_id']
    async with db.DatabaseBot("DataBase/db.db") as db_bot:
        await db_bot.add_geo_acc(sum_id, float(money))
           # await db_bot.commit()
    await bot.send_message(message.chat.id, text='Гео добавлено\n')
    await bot.send_message(message.chat.id, text='Админ панель', reply_markup=adm_kb.adm_menu)

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
    async with db.DatabaseBot("DataBase/db.db") as db_bot:
        user_info = await db_bot.get_user_bal(sum_id)
    if user_info[4] == '0':
        async with db.DatabaseBot("DataBase/db.db") as db_bot:
            await db_bot.add_sum(sum_id, float(money))
    else:
        final_balance = float(user_info[4]) + float(money)
        async with db.DatabaseBot("DataBase/db.db") as db_bot:
            await db_bot.update_sum(sum_id,final_balance)
    await bot.send_message(message.chat.id, text ='Баланс обновлён.\n'
                                                  f'Новый баланс пользователя {sum_id}: {float(final_balance)}$')
    await bot.send_message(message.chat.id, text ='Выберите нужные настройки', reply_markup=adm_kb.adm_menu)


if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)