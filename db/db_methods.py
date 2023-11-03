import asyncpg
import jsonpickle as jsonpickle
from asyncio import AbstractEventLoop
from typing import Any


class PoolManager:

    def __init__(self, **kwargs) -> None:
        self._db_auth_data = kwargs
        self._table_is_created = False # Можно переделать под сохранение статуса в Redis и проводить валидацию создания бд.


    async def __aenter__(self) -> asyncpg.Pool:
        self.pool = await asyncpg.create_pool(**self._db_auth_data)

        if not self._table_is_created:
            await self.pool.execute("""CREATE TABLE IF NOT EXISTS CDN_bot_table(
                                    user_id BIGINT NOT NULL PRIMARY KEY,
                                    chat_id BIGINT NOT NULL,
                                    username TEXT NOT NULL,
                                    customer_id VARCHAR(40),
                                    wallet_id VARCHAR(40),
                                    phone VARCHAR(11) NOT NULL,
                                    name TEXT NOT NULL)""")
            self._table_is_created = True

        return self.pool


    async def __aexit__(self, *args): 
        await self.pool.close()


class BotDataBase:

    def __init__(
            self, username: str, password: str, database: str,
            host: str = "localhost", port: int = 5432, dsn: str = None,
            loop: AbstractEventLoop = None
    ) -> None:
        self.__auth_data = {
            "host": host,
            "port": port,
            "user": username,
            "password": password,
            "database": database
        }

        if dsn is not None:
            self.__auth_data.clear()
            self.__auth_data.update({"dsn": dsn})

        if loop is not None:
            self.__auth_data.update({"loop": loop})

        self.__db = PoolManager(**self.__auth_data)


    async def set_user_data(self, user_id: int, chat_id: int, username: str, phone: str, name: str) -> None:
        async with self.__db as db:
            await db.execute("INSERT INTO CDN_bot_table (user_id, chat_id, username, phone, name)\
                             VALUES($1, $2, $3, $4, $5) \
                             ON CONFLICT (user_id) DO UPDATE SET chat_id = $2", 
                             user_id, chat_id, username, phone, name)


    async def update_customer_id(self, user_id: int, customer_id: str) -> None:
        async with self.__db as db:
            await db.execute("UPDATE CDN_bot_table \
                             SET customer_id=$1 \
                             WHERE user_id=$2", 
                             customer_id, user_id)


    async def update_wallet_id(self, user_id: int, wallet_id: str) -> None:
            async with self.__db as db:
                await db.execute("UPDATE CDN_bot_table \
                                 SET wallet_id=$1 \
                                 WHERE user_id=$2", 
                                 wallet_id, user_id)


    async def get_user_data(self, user_id: int) -> Any:
        async with self.__db as db:
            response = await db.fetchrow("SELECT user_id, username, customer_id, wallet_id, name, phone \
                                         FROM CDN_bot_table \
                                         WHERE user_id=$1", 
                                         user_id)
            return response


    async def get_user_id(self, user_id: int) -> Any:
            async with self.__db as db:
                response = await db.fetchval("SELECT user_id, \
                                            FROM CDN_bot_table \
                                            WHERE user_id=$1", 
                                            user_id)
                return response
