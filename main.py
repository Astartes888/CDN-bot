import asyncio
import dotenv
import uvicorn
from fastapi import FastAPI
#from bot_init import bot, dp
from api import webhook
from bot_init import bot, dp


app = FastAPI()
app.include_router(webhook.app_router)


#dotenv.load_dotenv()    # загружаем переменные окружения в текущее окружение из файла .env в текущей дериктории


async def main():

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
	asyncio.run(main())
    #uvicorn.run(app, host="127.0.0.1", port=8000)