from fastapi import FastAPI
from aiogram import types
from bot_main import logger, dp, bot, TOKEN


WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_URL = 'https://dfbb-45-152-121-39.ngrok-free.app' + WEBHOOK_PATH

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
    logger.info("Bot started")


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    logger.info("Bot stopped")


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)