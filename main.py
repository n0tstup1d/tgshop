from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils import executor

from LOLZTEAM import AutoUpdate, Constants
from LOLZTEAM.API import Forum, Market
from LOLZTEAM.Tweaks import DelaySync, SendAsAsync, CreateJob
from LOLZTEAM.Utils import CheckPayment
from LOLZTEAM.API import Market
from config import token_lolz
import requests

import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from datetime import date, datetime, timedelta
import Database.db as db
import config
'''import Keyboards.user_kb as user_kb
import Keyboards.adm_kb as adm_kb

import Payments.cryptobot as cryptobot'''
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
    await commands.set_default_commands(bot)
    async with db.DatabaseBot("Database/db.db") as db_bot:
        rez = await db_bot.check_users_start(message.from_user.id)
    if rez:
        pass
    else:
        current_date = date.today()
        async with db.DatabaseBot("Database/db.db") as db_bot:
            await db_bot.insert_user(message.from_user.id, current_date, arg)
    await bot.send_message(message.chat.id, text='Добро пожаловать', reply_markup=user_kb.main_menu)


@dp.message_handler(commands=['adm'])
async def adm(message:types.Message):
    if message.from_user.id in config.id_adm:
        await bot.send_message(message.chat.id,text = 'Добро пожаловать в админ панель')#reply_markup=adm_kb.adm_menu


@dp.message_handler(content_types=['text'])
async def text(message:types.Message):
    if message.text == "👤 Профиль":
        await bot.send_message(message.chat.id, f"Ваш ID: {message.chat.id}\n"
                                                f"Куплено аккаунтов: бд не подключенна\n"
                                                f"Может сделать на все товары как написанно выше ", reply_markup=user_kb.main_menu)
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
    if message.text == "💌 Получить код с почты":
        await bot.send_message(message.chat.id,"Введите вашу почту", reply_markup=await user_kb.mail_back_kb())
        await states.user_states.for_maill.set()
@dp.callback_query_handler(state=states.user_states.proxy)
async def user_states_accounts(call: CallbackQuery, state=FSMContext):
        await state.finish()
        if call.data == 'cancel_mail':
            await bot.edit_message_text('Введите id пользователя', call.message.chat.id, call.message.message_id,
                                        reply_markup=user_kb.main_menu)


if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)