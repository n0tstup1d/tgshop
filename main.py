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
        await bot.send_message(message.chat.id, f"--------- В наличии ---------\n",
                                                reply_markup=user_kb.main_menu)

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