import aiosqlite
import asyncio
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
                    CREATE TABLE "users" (
                    "id_users"	INTEGER,
	                "data_reg"	TEXT,
	                "sub_date"	TEXT,
	                "balance"	FLOAT,
	                PRIMARY KEY("id_users" AUTOINCREMENT)
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

    async def insert_user(self, user_id, date_reg, arg):

            async with self.lock:
                await self.db.execute('''
                    INSERT OR IGNORE INTO users (user_id, data_reg, sub_date, balance)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, date_reg, 0, 0,))
                await self.db.commit()

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