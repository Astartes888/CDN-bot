import logging
import aioredis
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums.parse_mode import ParseMode
from api.iiko_api_methods.methods import IikoTransport
from db.db_methods import BotDataBase
from config import load_config
from aiogram.loggers import event 

config = load_config()  # вызываем функцию конфига, возвращающая дата-класс Config с заполенными атрибутами из окружения 

TOKEN = config.tg_bot.token
ADMIN_ID = config.tg_bot.admin_id
API_TOKEN = config.api.api_token
ORG_ID = config.api.api_org_id
WEBHOOK_URL = config.webhook.webhook_url
DB_USER = config.db.db_user
DATABASE = config.db.database
DB_PASSWORD = config.db.db_password
REDIS_URL = config.db.redis_url

handler = TimedRotatingFileHandler(filename='bot_log.log', when='D', interval=31, backupCount=2)
logging.basicConfig(level=logging.INFO, 
                    handlers=[handler], 
                    format=u'%(filename)s:%(lineno)d #%(levelname)-6s [%(asctime)s] - %(name)s: %(message)s'
                    )
#event.setLevel(logging.ERROR) # изменяем уровень событий aiogram с info на error, чтобы не засорять логи 

logger = logging.getLogger()

redis = aioredis.from_url(REDIS_URL)
storage=RedisStorage(redis=redis)
bot_db = BotDataBase(username=DB_USER, password=DB_PASSWORD, database=DATABASE)
api = IikoTransport(API_TOKEN, logger=logger)
dp = Dispatcher(storage=storage)
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)