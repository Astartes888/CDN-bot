from fastapi import APIRouter
from aiogram import types
from bot_init import dp, bot, TOKEN, logger, WEBHOOK_URL


WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_FULL_URL = WEBHOOK_URL + WEBHOOK_PATH
#cert = types.FSInputFile('/home/nod888/certs/city_bot.pem')

app_router = APIRouter()


@app_router.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_FULL_URL or webhook_info.allowed_updates is True:
        await bot.set_webhook(url=WEBHOOK_FULL_URL, allowed_updates=[])
    logger.info("Bot started")


@app_router.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


@app_router.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    logger.info("Bot stopped")
