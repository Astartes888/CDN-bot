import json
from aiogram import Router
from aiogram import F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType
from text.bot_reply import bot_text
from states.bot_states import FSM_bot
from buttons.buttons_factory import KeyboardFabric
from text.button_text import menu_text


router = Router()


@router.message(StateFilter(default_state), F.content_type == ContentType.WEB_APP_DATA)
async def get_app_data(message: Message, state: FSMContext):
    data = json.loads(message.web_app_data.data)
    try:
        pass # вызов функции (метода) для записи данных в бд
        await state.set_state(FSM_bot.user_menu)
        keyboard = await KeyboardFabric.get_markup(2, *menu_text, resize=True)
        await message.answer(bot_text['greetings'], reply_markup=keyboard)
        await message.answer(str(data))
    except:
        print('Какая то ошибка') # перехватываем исключение и отправляем сообщение об ошибке с кнопкой web_app
