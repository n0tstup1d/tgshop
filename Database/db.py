import aiosqlite
import asyncio
import pytz
from datetime import datetime, timedelta

import traceback


class DatabaseBot:
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = None
        self.lock = asyncio.Lock()

    async def connect(self):
        if self.db is None:
            self.db = await aiosqlite.connect(self.db_file)

    async def close(self):
        if self.db:
            await self.db.close()
            self.db = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def initialize_db(self):
        async with self.lock:
            await self.connect()

            result = await self.db.execute("""
                SELECT name 
                FROM sqlite_master 
                WHERE type='table'
                AND name IN ('accounts')
            """)
            print(result)
            existing_tables = [row[0] for row in await result.fetchall()]
            print(existing_tables)
            if 'accounts' not in existing_tables:
                await self.db.execute('''
                    CREATE TABLE "accounts" (
                    "id_accounts"	INTEGER,
                    "accounts"	INTEGER,
                    "date"	TEXT,
                    PRIMARY KEY("id_accounts" AUTOINCREMENT)
                )
                ''')
            if 'users' not in existing_tables:
                await self.db.execute('''
                        CREATE TABLE users (
                        id_users	INTEGER,
                        data_reg	TEXT,
                        sub_date	TEXT,
                        counts_accounts	TEXT,
                        PRIMARY KEY("id_users" AUTOINCREMENT)
                    )
                ''')
            if 'cart' not in existing_tables:
                await self.db.execute('''
                            CREATE TABLE IF NOT EXISTS cart (
                                id_cart	INTEGER,
                                user_id	INTEGER,
                                item	TEXT,
                                count_item	INTEGER,
                                price_cart	FLOAT,
                                added_at	TIMESTAMP,
                                PRIMARY KEY("id_cart" AUTOINCREMENT)
                            )
                        ''')

            await self.db.commit()

    async def get_accounts(self, account):
            async with self.lock:
                try:
                    async with self.db.execute('SELECT * FROM accounts WHERE accounts = ?', (account,)) as cursor:
                        res = await cursor.fetchone()
                        return res
                except:
                    return False

    async def check_users_start(self, user_id):
            async with self.lock:
                async with self.db.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,)) as cursor:
                    res = await cursor.fetchone()
                    return bool(res)

    async def check_accounts(self, user_id):
            async with self.lock:
                async with self.db.execute('SELECT * FROM accounts WHERE date_cookie = ?', (user_id,)) as cursor:
                    res = await cursor.fetchone()
                    return bool(res)

    async def check_accounts_for_cookie_true(self, user_id):
            async with self.lock:
                async with self.db.execute('SELECT accounts FROM accounts WHERE accounts LIKE ?', (f'%{user_id}%',)) as cursor:
                    res = await cursor.fetchone()
                    return bool(res)

    async def check_accounts_for_cookie(self, user_id):
            async with self.lock:
                async with self.db.execute('SELECT accounts FROM accounts WHERE accounts LIKE ?', (f'%{user_id}%',)) as cursor:
                    res = await cursor.fetchone()
                    return res

    async def check_users_sub(self, user_id):
            async with self.lock:
                async with self.db.execute('SELECT sub_date FROM users WHERE user_id = ?', (user_id,)) as cursor:
                    res = await cursor.fetchone()
                    return str(res)

    async def check_users_mon(self, user_id):
            async with self.lock:
                async with self.db.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)) as cursor:
                    res = await cursor.fetchone()
                    return float(res)

    async def add_sum(self, user_id, money):
        async with self.lock:
            await self.db.execute('UPDATE users SET balance = ? WHERE user_id = ?', ( int(money) , user_id))
            await self.db.commit()

    async def update_sum(self, user_id, final_balance):
        async with self.lock:
            await self.db.execute('UPDATE users SET balance = ? WHERE user_id = ?', ( final_balance , user_id))
            await self.db.commit()

    async def get_user_bal(self, user_id):
        async with self.lock:
            async with self.db.execute('SELECT counts_accounts FROM users WHERE user_id = ?', (user_id,)) as cursor:
                res = await cursor.fetchone()
                return res[0] if res else None

    async def insert_user(self, user_id, date_reg, arg):
            async with self.lock:
                await self.db.execute('''
                    INSERT OR IGNORE INTO users (user_id, data_reg, sub_date, counts_accounts)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, date_reg, arg, 0))
                await self.db.commit()

    async def insert_temp_accounts(self, user_id, date_reg):
            async with self.lock:
                await self.db.execute('''
                    INSERT OR IGNORE INTO temp_acc (accounts, date_add)
                    VALUES (?, ?)
                ''', (user_id, date_reg))
                await self.db.commit()

    async def add_geo_acc(self, user_id, name, final_balance):
        async with self.lock:
            await self.db.execute('INSERT OR IGNORE INTO countries (region, names,price ) VALUES (?, ?, ?)',
                                          (user_id, name,final_balance))
            await self.db.commit()

    '''async def add_cart_acc(self, geo, price, count):
        async with self.lock:
            await self.db.execute('INSERT OR IGNORE INTO cart (region, price ) VALUES (?, ?)',(user_id, final_balance))
            await self.db.commit()'''

    async def add_item(self, user_id, region,item, price, count_item):
        async with self.lock:
            await self.db.execute('''
                INSERT INTO cart (user_id, region, item, count_item, price_cart, added_at) VALUES (?, ?, ?, ?, ?,CURRENT_TIMESTAMP)
            ''', (user_id, region,item, count_item, price,))
            await self.db.commit()

    async def get_items(self, user_id):
        async with self.lock:
            async with self.db.execute('''
                SELECT count_item, region, price_cart FROM cart WHERE user_id = ?
            ''', (user_id,)) as cursor:
                rows = await cursor.fetchall()
        return rows

    async def get_item(self, user_id):
        async with self.lock:
            async with self.db.execute('''
                SELECT item FROM cart WHERE user_id = ?
            ''', (user_id,)) as cursor:     #, region = ?, count_item = ?
                rows = await cursor.fetchall()
        return rows

    async def sum_count_acc(self, user_id):
        async with self.lock:
            async with self.db.execute('''
                SELECT SUM(count_item) FROM cart WHERE user_id = ?
            ''', (user_id,)) as cursor:
                res = await cursor.fetchone()
                return res[0] if res else None

    async def get_count_geo(self, geo):
        async with self.lock:
            async with self.db.execute('SELECT COUNT(geo_acc) FROM accounts WHERE geo_acc = ?', (geo,)) as cursor:
                res = await cursor.fetchone()
                return res[0]

    async def get_select_geo_min_4(self, geo):
        # Вычисляем время 4 часа назад от текущего времени UTC
        four_hours_ago = datetime.utcnow() - timedelta(hours=4)
        formatted_time = four_hours_ago.strftime('%Y-%m-%d %H:%M:%S')

        async with self.lock:
            query = '''
                SELECT accounts
                FROM accounts
                WHERE geo_acc = ? AND date_add > ?
            '''
            async with self.db.execute(query, (geo, formatted_time)) as cursor:
                res = await cursor.fetchone()
                return res[0] if res else None

    async def get_acc_less_than_4_hours(self, limit, geo):
        now = datetime.utcnow()
        max_time = now - timedelta(hours=4)

        query = """
        SELECT accounts FROM accounts
        WHERE date_add > ?
        AND geo_acc = ?
        LIMIT ?
        """

        async with self.lock:
            async with self.db.execute(query, (max_time, geo, limit)) as cursor:
                rows = await cursor.fetchall()
        return [row[0] for row in rows]

    async def get_acc_between_4_and_12_hours(self, limit, geo):
        now = datetime.utcnow()
        min_time = now - timedelta(hours=12)
        max_time = now - timedelta(hours=4)

        query = """
        SELECT accounts FROM accounts
        WHERE ? > date_add < ?
        AND geo_acc = ?
        LIMIT ?
        """

        async with self.lock:
            async with self.db.execute(query, (min_time, max_time, geo, limit)) as cursor:
                rows = await cursor.fetchall()
        return [row[0] for row in rows]

    async def get_acc_min_24_max12(self, limit, geo):
        now = datetime.utcnow()
        min_time = now - timedelta(hours=24)
        max_time = now - timedelta(hours=12)

        query = """
        SELECT accounts FROM accounts
        WHERE ? > date_add < ?
        AND geo_acc = ?
        LIMIT ?
        """

        async with self.lock:
            async with self.db.execute(query, (min_time, max_time,geo, limit)) as cursor:
                rows = await cursor.fetchall()
        return [row[0] for row in rows]

    async def get_acc_between_24_and_36_hours(self, limit, geo):
        now = datetime.utcnow()
        min_time = now - timedelta(hours=36)
        max_time = now - timedelta(hours=24)


        print(f"min_time: {min_time}, max_time: {max_time}, geo: {geo}, limit: {limit}")

        query = """
        SELECT accounts FROM accounts
        WHERE ? > date_add < ?
        AND geo_acc = ?
        LIMIT ?
        """

        async with self.lock:
            try:
                async with self.db.execute(query, (min_time, max_time, geo, limit)) as cursor:
                    rows = await cursor.fetchall()
                    print(f"Query returned: {rows}")
            except Exception as e:
                print(f"Error executing query: {e}")

        return [row[0] for row in rows]

    async def get_acc_greater_than_36_hours(self, limit, geo):
        now = datetime.utcnow()
        min_time = now - timedelta(hours=36)

        query = """
        SELECT accounts FROM accounts
        WHERE date_add < ?
        AND geo_acc = ?
        LIMIT ?
        """

        async with self.lock:
            async with self.db.execute(query, (min_time, geo, limit)) as cursor:
                rows = await cursor.fetchall()
        return [row[0] for row in rows]

    async def get_select_geo_by_tips(self, geo, tips, limit):
        # Вычисляем временные метки для каждого временного диапазона
        now = datetime.utcnow()
        time_intervals = {
            '2': (now - timedelta(hours=4), now - timedelta(hours=12)),
            '3': (now - timedelta(hours=12), now - timedelta(days=1)),
            '4': (now - timedelta(days=1), now - timedelta(hours=36)),
            '5': (now - timedelta(hours=36), None)
        }

        # Определяем временной диапазон для запроса на основе tips
        if tips == '1':
            query_time = (now - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')
            query = '''
                SELECT accounts
                FROM accounts
                WHERE geo_acc = ? AND date_add > ?
                LIMIT ?
            '''
            query_params = (geo, query_time, limit)
        elif tips in time_intervals:
            start_time, end_time = time_intervals[tips]
            query = '''
                SELECT accounts
                FROM accounts
                WHERE geo_acc = ? AND date_add > ? AND date_add <= ?
                LIMIT ?
            ''' if end_time else '''
                SELECT accounts
                FROM accounts
                WHERE geo_acc = ? AND date_add <= ?
                LIMIT ?
            '''
            query_params = (
            geo, start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S') if end_time else None,
            limit)
        else:
            # Если `tips` не соответствует ни одному из известных значений, вернем None
            return None

        async with self.lock:
            async with self.db.execute(query, query_params) as cursor:
                res = await cursor.fetchall()
                if res:
                    # Формируем строку, разделенную запятыми
                    return ','.join(row[0] for row in res)
                else:
                    return None

    async def get__geo(self, geo):
        now = datetime.now()
        intervals = [
            ("less_4h", now - timedelta(hours=4)),
            ("more_4h_less_12h", now - timedelta(hours=4), now - timedelta(hours=12)),
            ("more_12h_less_24h", now - timedelta(hours=12), now - timedelta(hours=24)),
            ("more_24h_less_36h", now - timedelta(hours=24), now - timedelta(hours=36)),
            ("more_36h", now - timedelta(hours=36)),
        ]
        counts = {}
        async with self.db.cursor() as cursor:
            for interval in intervals:
                if interval[0] == "less_4h":
                    await cursor.execute("SELECT COUNT(*) FROM accounts WHERE geo_acc = ? AND date_add >= ?",
                                         (geo, interval[1]))
                elif interval[0] == "more_36h":
                    await cursor.execute("SELECT COUNT(*) FROM accounts WHERE geo_acc = ? AND date_add < ?",
                                         (geo, interval[1]))
                else:
                    await cursor.execute(
                        "SELECT COUNT(*) FROM accounts WHERE geo_acc = ? AND date_add < ? AND date_add >= ?",
                        (geo, interval[1], interval[2]))
                result = await cursor.fetchone()
                counts[interval[0]] = result[0]
        return counts

    async def get_all_users(self):
        async with self.lock:
            async with self.db.execute('SELECT * FROM users') as cursor:
                res = await cursor.fetchall()
                return res

    async def sum_last_24_hours(self):
        now = datetime.now()
        last_24_hours = now - timedelta(days=1)
        async with self.lock:
            cursor = await self.db.execute('''
                SELECT SUM(price) FROM checks
                WHERE date_create >= ?
            ''', (last_24_hours.strftime('%Y-%m-%d %H:%M'),))
            result = await cursor.fetchone()
            return result[0] if result[0] is not None else 0.0

    async def sum_last_week(self):
        now = datetime.now()
        last_week = now - timedelta(weeks=1)
        async with self.lock:
            cursor = await self.db.execute('''
                SELECT SUM(price) FROM checks
                WHERE date_create >= ?
            ''', (last_week.strftime('%Y-%m-%d %H:%M'),))
            result = await cursor.fetchone()
            return result[0] if result[0] is not None else 0.0

    async def sum_last_month(self):
        now = datetime.now()
        last_month = now - timedelta(days=30)
        async with self.lock:
            cursor = await self.db.execute('''
                SELECT SUM(price) FROM checks
                WHERE date_create >= ?
            ''', (last_month.strftime('%Y-%m-%d %H:%M'),))
            result = await cursor.fetchone()
            return result[0] if result[0] is not None else 0.0

    async def get_accounts_from(self,geo):
        async with self.lock:
            cursor = await self.db.execute('''
                SELECT accounts FROM accounts 
                WHERE geo_acc = ?
            ''',(geo,))
            accounts = await cursor.fetchall()
            return accounts

    async def get_old_items(self):
        async with self.lock:
            async with self.db.execute('''SELECT item FROM cart WHERE added_at < datetime('now', '-30 minutes')''') as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]

    '''async def get_date_cookie_accounts(self, cookie):
        async with self.lock:
            async with self.db.execute(''SELECT cookie_accs FROM accounts WHERE accounts = ?'',(cookie,)) as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]
    '''
    async def get_cookie_accounts(self, cookie):
        async with self.lock:
            async with self.db.execute('''SELECT cookie_accs FROM accounts WHERE accounts = ?''',(cookie,)) as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]

    async def get_all_accounts(self):
        async with self.lock:
            async with self.db.execute('''SELECT accounts FROM accounts WHERE date_cookie < datetime('now', '-480 minutes')''') as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]

    async def get_counts_user(self):
        async with self.lock:
            async with self.db.execute('SELECT count(user_id) FROM users') as cursor:
                res = await cursor.fetchone()
                return res[0]

    async def delete_old_items(self):
        async with self.lock:
            await self.db.execute('''DELETE FROM cart WHERE added_at < datetime('now', '-30 minutes')''')
            await self.db.commit()

    async def delete_concret_accs(self, geo):
        async with self.lock:
            await self.db.execute('''DELETE FROM accounts WHERE geo_acc = ?''',(geo,))
            await self.db.commit()

    async def delete_account_cookie(self, geo):
        async with self.lock:
            await self.db.execute('''DELETE FROM accounts WHERE accounts = ?''',(geo,))
            await self.db.commit()

    async def delete_temp_accs(self, geo):
        async with self.lock:
            await self.db.execute('''DELETE FROM temp_acc WHERE accounts = ?''',(geo,))
            await self.db.commit()

    async def delete_all_accs(self):
        async with self.lock:
            await self.db.execute('''DELETE FROM accounts''')
            await self.db.commit()

    async def del_geo_acc(self, phonk_id):
        async with self.lock:
            await self.db.execute('DELETE FROM countries WHERE region = ?', (phonk_id,))
            await self.db.commit()

    async def get_id_cart(self, user_id):
        async with self.lock:
            async with self.db.execute('''
                SELECT id_cart FROM cart WHERE user_id = ?
            ''', (user_id,)) as cursor:
                rows = await cursor.fetchall()
        return rows

    async def get_price_country(self, geo):
        async with self.lock:
            async with self.db.execute('''SELECT price FROM countries WHERE region = ?''', (geo,)) as cursor:
                rows = await cursor.fetchall()
        return rows[0]

    async def update_balance_user_plus(self, user_id, money):
        async with self.lock:
            await self.db.execute('UPDATE users SET balance = ? WHERE user_id = ?', (float(money), user_id,))
            await self.db.commit()

    async def update_balance_user(self, user_id, money):
        async with self.lock:
            await self.db.execute('UPDATE users SET counts_accounts = ? WHERE user_id = ?', (int(money), user_id,))
            await self.db.commit()

    async def delete_item(self, user_id):
        async with self.lock:
            await self.db.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
            await self.db.commit()

    async def delete_item_item(self, item):
        async with self.lock:
            await self.db.execute('DELETE FROM accounts WHERE accounts = ?', (item,))
            await self.db.commit()

    async def insert_purchase(self, sum_purchase: int):
        date_purchase = datetime.now().strftime('%Y-%m-%d %H:%M')  # Форматирование даты до минуты
        async with self.lock:
            await self.db.execute('''
                INSERT INTO purchase (date_purchase, sum_purchase)
                VALUES (?, ?)
            ''', (date_purchase, sum_purchase))
            await self.db.commit()

    async def insert_trash_accs(self, sum_purchase):
        async with self.lock:
            await self.db.execute('''
                INSERT INTO trash_accs_cookie (trash_accs)
                VALUES (?)
            ''', (sum_purchase))
            await self.db.commit()

    async def insert_check(self, sum_purchase, number_check, user_id, string):
        date_purchase = datetime.now().strftime('%Y-%m-%d %H:%M')  # Форматирование даты до минуты
        async with self.lock:
            await self.db.execute('INSERT INTO checks (number_check, user_id, date_create, price, items) VALUES (?, ?, ?, ?, ?) ', (number_check, user_id, date_purchase, sum_purchase, string))
            await self.db.commit()

    async def insert_account(self, geo_acc, accounts):  # Форматирование даты до минуты
        date_purchase = datetime.now().strftime('%Y-%m-%d %H:%M')
        async with self.lock:
            await self.db.execute('INSERT INTO accounts (geo_acc, accounts, date_add) VALUES (?, ?, ?) ', (geo_acc, accounts, date_purchase))
            await self.db.commit()

    async def insert_account_cookie(self, account,geo_acc):  # Форматирование даты до минуты
        date_purchase = datetime.now().strftime('%Y-%m-%d %H:%M')

        async with self.lock:
            await self.db.execute(
                'UPDATE accounts SET cookie_accs = ?, date_cookie = ? WHERE accounts = ?',
                (geo_acc, date_purchase, account)
            )
            await self.db.commit()

    async def update_account_cookie(self, account):  # Форматирование даты до минуты
        date_purchase = datetime.now().strftime('%Y-%m-%d %H:%M')
        async with self.lock:
            await self.db.execute(
                'UPDATE accounts SET date_cookie = ? WHERE accounts = ?',
                (date_purchase, account,)
            )
            await self.db.commit()

    async def insert_accounts(self, geo_acc, accounts, date_purchase):  # Форматирование даты до минуты
        async with self.lock:
            await self.db.execute('INSERT INTO accounts (geo_acc, accounts, date_add) VALUES (?, ?, ?) ', (geo_acc, accounts, date_purchase))
            await self.db.commit()

    async def insert_account_old(self, geo_acc, accounts,old): # Форматирование даты до минуты
        async with self.lock:
            await self.db.execute('INSERT INTO accounts (geo_acc, accounts, date_add) VALUES (?, ?, ?) ', (geo_acc, accounts, old))
            await self.db.commit()

    async def select_temp_accounts(self, user_id):
        async with self.lock:
            async with self.db.execute('SELECT date_add FROM temp_acc WHERE accounts = ?', (user_id,)) as cursor:
                res = await cursor.fetchone()
                return res

    async def select_date_acc(self, user_id):
        async with self.lock:
            async with self.db.execute('SELECT date_add FROM accounts WHERE accounts = ?', (user_id,)) as cursor:
                res = await cursor.fetchone()
                return res

    async def get_user_info(self, user_id):
        async with self.lock:
            async with self.db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)) as cursor:
                res = await cursor.fetchone()
                return res

    async def get_countries_sum(self, country_name):
        async with self.lock:
            async with self.db.execute('SELECT * FROM countries WHERE region = ?', (country_name,)) as cursor:
                res = await cursor.fetchone()
                return res


    async def update_geo_acc(self, user_id, final_balance):
        async with self.lock:
            await self.db.execute('UPDATE countries SET price = ? WHERE region = ?', ( final_balance , user_id))
            await self.db.commit()


    async def get_countries_acc(self):
            async with self.lock:
                async with self.db.execute('SELECT region, price, names FROM countries') as cursor:
                    rows = await cursor.fetchall()
            return rows

    async def get_count_acc(self):
            async with self.lock:
                async with self.db.execute('SELECT region FROM countries') as cursor:
                    rows = await cursor.fetchall()
            return rows

    async def get_count_acc_sum(self, geo):
            async with self.lock:
                async with self.db.execute('SELECT price FROM countries WHERE region = ?',(geo,)) as cursor:
                    rows = await cursor.fetchall()
            return rows

    async def get_names_countries_acc(self, region):
        async with self.lock:
            async with self.db.execute('SELECT names FROM countries WHERE region = ?', (region,)) as cursor:
                res = await cursor.fetchone()
                return res[0] if res else None



async def main():
    database_bot = DatabaseBot("Database/db.db")
    await database_bot.initialize_db()
    # await database_bot.check_if_row_exists("phone_info", "account_names", "")
    # await database_bot.check_if_row_exists("users", "last_video_send", 0)
    # await database_bot.check_if_row_exists("users", "sended_videos", 0)
    # await database_bot.check_if_row_exists("phone_info", "nicknames", "")

# async def main():
#     database_bot = DatabaseBot("bd.db")
#     await database_bot.initialize_db()


#asyncio.run(main())