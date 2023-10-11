import logging
import aioredis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from api.iiko_api_methods.methods import IikoTransport
from db.db_methods import BotDataBase
from config import load_config

config = load_config()  # вызываем функцию конфига, возвращающая дата-класс Config с заполенными атрибутами из окружения 

TOKEN = config.tg_bot.token
ADMIN_ID = config.tg_bot.admin_id
API_TOKEN = config.api.api_token
ORG_ID = config.api.api_org_id
WEBHOOK_URL = ''
DB_USER = config.db.db_user
DATABASE = config.db.database
DB_PASSWORD = config.db.db_password
REDIS_URL = config.db.redis_url
#TOKEN = '6635237394:AAHT6iZDv5ZtnXVrejO7oaQRp6llrYebv4k'
#API_TOKEN = 'ebd53133-dd1'
#ORG_ID = '2ccfa2c5-95e7-4a6a-b0be-e96bef2cf7ec'

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, 
                    filename="bot_log.log",
                    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
                    )
redis = aioredis.from_url(REDIS_URL)
storage=RedisStorage(redis=redis)
bot_db = BotDataBase(username=DB_USER, password=DB_PASSWORD, database=DATABASE)
api = IikoTransport(API_TOKEN, logger=logger)
dp = Dispatcher(storage=storage)
bot = Bot(token=TOKEN)