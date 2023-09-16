from aiogram import Router
from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from buttons.buttons_factory import KeyboardFabric
from states.bot_states import FSM_bot
from text.button_text import button_text


router = Router()


@router.message(Command(commands=['admin'])) #F.from_user.id == 913548059
async def admin_menu(message: Message, state: FSMContext):
    await state.set_state(FSM_bot.admin_menu)
    keyboard = await KeyboardFabric.get_markup(1, button_text['exit'], resize=True)
    await message.answer(text=f'Ваш ID: {message.from_user.id} Ваш ник: @{message.from_user.username}', reply_markup=keyboard)


@router.message(F.text =='Выход', StateFilter(FSM_bot.admin_menu))
async def admin_menu(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer(text=f'Введите команду /start для работы как обычный пользователь')