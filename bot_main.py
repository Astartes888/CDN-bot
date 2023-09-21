import asyncio
import logging
import aioredis
import dotenv
import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from handlers import user_handlers, admin_handlers, data_handlers
#from fsm_storage.postgresql import PGStorage 
from api.webhook import app
from config import load_config


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="bot_log.log",
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)


#config = load_config()  # вызываем функцию конфига, возвращающая дата-класс Config с заполенными атрибутами из окружения 
#dotenv.load_dotenv()    # загружаем переменные окружения в текущее окружение из файла .env в текущей дериктории


#TOKEN = ''
TOKEN = '6635237394:AAHT6iZDv5ZtnXVrejO7oaQRp6llrYebv4k'
#storage = PGStorage(username='postgres', password='holynet', database='postgres')
redis = aioredis.from_url('redis://195.133.201.150:6379')
storage=RedisStorage(redis=redis)
dp = Dispatcher(storage=storage)
bot = Bot(token=TOKEN)
dp.include_routers(user_handlers.router, admin_handlers.router, data_handlers.router)


# async def main():
    

#     bot = Bot(token=TOKEN)
#     dp = Dispatcher(storage=storage)
	
#     dp.include_routers(user_handlers.router, admin_handlers.router, data_handlers.router)

#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot)
    

if __name__ == "__main__":
	#asyncio.run(main())
    uvicorn.run(app, host="127.0.0.1", port=8000)