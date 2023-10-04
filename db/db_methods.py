import asyncpg
import jsonpickle as jsonpickle
from asyncio import AbstractEventLoop
from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType
from typing import Any


class PoolManager:
    __slots__ = ("_db_auth_data", "_tables_is_created", "pool")

    def __init__(self, **kwargs) -> None:
        self._db_auth_data = kwargs
<<<<<<< HEAD
        self._tables_is_created = False # Можно переделать под сохранение статуса в Redis и проводить валидацию создания бд.
=======
        self._table_is_created = False # Можно переделать под сохранение статуса в Redis и проводить валидацию создания бд.

>>>>>>> 8c40f6ce643255b1bdfb251d8011bb31fcbeb8b6

    async def __aenter__(self) -> asyncpg.Pool:
        self.pool = await asyncpg.create_pool(**self._db_auth_data)

<<<<<<< HEAD
        if not self._tables_is_created:
=======
        if not self._table_is_created:
>>>>>>> 8c40f6ce643255b1bdfb251d8011bb31fcbeb8b6
            await self.pool.execute("""CREATE TABLE IF NOT EXISTS CDN_bot_table(
                                    user_id BIGINT NOT NULL PRIMARY KEY,
                                    chat_id BIGINT NOT NULL,
                                    username TEXT NOT NULL,
                                    customer_id VARCHAR(40),
                                    phone VARCHAR(11) NOT NULL,
                                    name TEXT NOT NULL)""")
<<<<<<< HEAD
            self._tables_is_created = True

        return self.pool

=======
            self._table_is_created = True

        return self.pool


>>>>>>> 8c40f6ce643255b1bdfb251d8011bb31fcbeb8b6
    async def __aexit__(self, *args): 
        await self.pool.close()


<<<<<<< HEAD
class BotDataBase():
=======
class BotDataBase:
>>>>>>> 8c40f6ce643255b1bdfb251d8011bb31fcbeb8b6
    __slots__ = ("host", "port", "username", "password", "database", "dsn", "loop")

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

<<<<<<< HEAD
    async def set_data(self, user_id: int, chat_id: int, username: str, phone: str, name: str) -> None:
=======

    async def set_user_data(self, user_id: int, chat_id: int, username: str, phone: str, name: str) -> None:
>>>>>>> 8c40f6ce643255b1bdfb251d8011bb31fcbeb8b6
        async with self.__db as db:
            await db.execute("INSERT INTO CDN_bot_table (user_id, chat_id, username, phone, name)\
                             VALUES($1, $2, $3, $4, $5) ON CONFLICT (user_id) DO UPDATE SET chat_id = $2", 
                             user_id, chat_id, username, phone, name)


<<<<<<< HEAD
    # async def get_state(self, key: StorageKey) -> str|None:
    #     async with self.__db as db:
    #         response = await db.fetchval("SELECT state FROM aiogram_state WHERE key=$1", jsonpickle.dumps(key))
    #         # response = await db.fetchval("SELECT state FROM aiogram_state WHERE user_id=$1 AND chat_id=$2", key.user_id, key.chat_id) #"SELECT \"state\" FROM \"AiogramLegacyStates\" WHERE key=$1"
    #         return response

    # async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
    #     async with self.__db as db:
    #         await db.execute("INSERT INTO aiogram_data VALUES($1, $2) ON CONFLICT (key) DO UPDATE SET data = $2", jsonpickle.dumps(key), jsonpickle.dumps(data))
    #         # await db.execute("INSERT INTO aiogram_data VALUES($1, $2, $3, $4) ON CONFLICT (user_id) DO UPDATE SET data = $4", 
    #         #                  key.user_id, key.chat_id, key.bot_id, jsonpickle.dumps(data)
    #         #                  ) #"INSERT INTO \"AiogramLegacyData\" VALUES($1, $2)"

    # async def get_data(self, key: StorageKey) -> dict[str, Any]:
    #     async with self.__db as db:
    #         response = await db.fetchval("SELECT data FROM aiogram_data WHERE key=$1", jsonpickle.dumps(key))
    #         #response = await db.fetchval("SELECT data FROM aiogram_data WHERE user_id=$1 AND chat_id=$2", key.user_id, key.chat_id) #"SELECT \"data\" FROM \"AiogramLegacyData\" WHERE key=$1"
    #         return jsonpickle.loads(response)

    # async def update_data(self, key: StorageKey, data: dict[str, Any]) -> dict[str, Any]:
    #     async with self.__db as db:
    #         response = await db.fetchval("UPDATE aiogram_data SET data=$1 WHERE key=$2 RETURNING data", jsonpickle.dumps(data), jsonpickle.dumps(key))
    #         # response = await db.fetchval("UPDATE aiogram_data SET data=$1 WHERE user_id=$2 AND chat_id=$3 RETURNING data", #"UPDATE \"AiogramLegacyData\" SET data=$1 WHERE key=$2 RETURNING data"
    #         #     jsonpickle.dumps(data), key.user_id, key.chat_id
    #         # )
    #         return jsonpickle.loads(response)
=======
    async def update_customer_id(self, user_id: int, customer_id: str) -> None:
        async with self.__db as db:
            await db.execute("UPDATE CDN_bot_table SET customer_id=$1 WHERE user_id=$2", customer_id, user_id)


    async def get_user_data(self, user_id: int) -> Any:
        async with self.__db as db:
            response = await db.fetchval("SELECT username, customer_id, name, phone FROM CDN_bot_table WHERE user_id=$1", user_id)
            return response
>>>>>>> 8c40f6ce643255b1bdfb251d8011bb31fcbeb8b6

