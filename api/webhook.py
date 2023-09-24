from fastapi import APIRouter
from aiogram import types
import uvicorn
from bot_init import dp, bot, TOKEN, logger


WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_URL = 'https://648f-45-152-121-39.ngrok-free.app' + WEBHOOK_PATH


app_router = APIRouter()


@app_router.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
    logger.info("Bot started")


@app_router.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


@app_router.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    logger.info("Bot stopped")
