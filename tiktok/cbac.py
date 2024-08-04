import requests
import json
import time
import os
import imaplib
import re
import email
import random
import config
import asyncio
import Database.db as db
import psutil
import signal
import traceback
import atexit
from config import api_key
from datetime import datetime, timedelta

PROXIES_FILE_PATH = 'proxy.txt'


async def init_db():
    database_bot = db.DatabaseBot("DataBase//db.db")
    await database_bot.connect()
    return database_bot


def get_proxy():
    try:
        with open(PROXIES_FILE_PATH, 'r') as file:
            proxies = file.readlines()
            proxy = proxies[1]
            print(proxy)
            parts = proxy.strip().split('|')
            ip_port_login_pass = parts[0].split(':')
            refresh_link = parts[1]
            ip = ip_port_login_pass[0]
            port = ip_port_login_pass[1]
            login = ip_port_login_pass[2]
            proxy_password = ip_port_login_pass[3]
            yield f"http://{login}:{proxy_password}@{ip}:{port}", refresh_link
    except Exception as e:
        print(f"Ошибка при чтении файла {PROXIES_FILE_PATH}:", e)
        requests.get(
            f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id=646534367&text=Ошибка чтения из файла прокси')
        return None

def start_work(account):
    database_bot = asyncio.run(init_db())
    print(account)
    accounts = account.split(':')
    geo_acc = accounts[0]
    login_acc = accounts[1]
    version = "34.9.3"
    while True:
        print(login_acc)
        with open(f'emp/{login_acc}.json', 'r') as file:
            data = json.load(file)

        device = data.get("device")
        cookie = data.get("cookie")

        proxy, refresh_link = next(get_proxy())

        print(proxy)

        print(proxy)
        date_purchase = datetime.now().strftime('%Y-%m-%d %H:%M')
        print(device)
        print(cookie)
        url = f"https://api.tokapi.online/v1/user/self?app_version={version}"
        get_headers = {
            "accept": "application/json",
            "x-api-key": f"{api_key}",
            "x-proxy": f"{proxy}",
            "x-device": f"{device}",
            "x-cookie": f"{cookie}",
            "x-project-name": 'tokapi'
        }
        response = requests.get(url, headers=get_headers)

        if response.status_code == 200:
            print(response.text)
            data = json.loads(response.text)
            user_id_acc = data['user']['uid']

        else:
            print(f"Нет доступа к аккаунту {response.text}")
            asyncio.run(database_bot.insert_trash_accs(account))
            asyncio.run(database_bot.delete_account_cookie(account))
            requests.get(
                f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id=646534367&text= Удалено из БД аккаунт {account}')
            current_pid = os.getpid()
            os.kill(current_pid, signal.SIGTERM)
            print(f"Process  with PID {current_pid} killed.")
            break

        url = f"https://api.tokapi.online/v1/user/{user_id_acc}/profile?app_version={version}"

        payload = {
            "profile": {
                "signature": f"{str(date_purchase)}"
            }
        }

        get_headers = {
            "accept": "application/json",
            "x-api-key": f"{api_key}",
            "x-proxy": f"{proxy}",
            "x-device": f"{device}",
            "x-cookie": f"{cookie}",
            "x-project-name": 'tokapi'
        }

        response = requests.post(url, json=payload, headers=get_headers)

        if response.status_code == 200:
            print('Аккаунт успешно обновлен')
            asyncio.run(database_bot.update_account_cookie(account))
            current_pid = os.getpid()
            os.kill(current_pid, signal.SIGTERM)
            print(f"Process  with PID {current_pid} killed.")
            break


        else:
            print(response.status_code)
            print(response.text)
            asyncio.run(database_bot.insert_trash_accs(account))
            requests.get(
                f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id=646534367&text= Удалено из БД аккаунт {account}')
            asyncio.run(database_bot.delete_account_cookie(account))
            current_pid = os.getpid()
            os.kill(current_pid, signal.SIGTERM)
            print(f"Process  with PID {current_pid} killed.")
            break