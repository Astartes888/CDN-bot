import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage 
from handlers import user_handlers, admin_handlers, data_handlers 


TOKEN = '6635237394:AAHT6iZDv5ZtnXVrejO7oaQRp6llrYebv4k'
#storage = PGStorage(username='postgres', password='holynet', db_name='PostgreSQL 15')
storage=MemoryStorage()


async def main():
    logging.basicConfig(level=logging.WARNING, filename="bot_log.log", format="%(asctime)s %(levelname)s %(message)s")

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)
	
    dp.include_routers(user_handlers.router, admin_handlers.router, data_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
	asyncio.run(main())