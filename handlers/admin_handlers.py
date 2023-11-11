from aiogram import Router
from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from buttons.buttons_factory import KeyboardFactory
from states.bot_states import FSM_bot
from text.button_text import button_text
from states.bot_states import FSM_bot
from bot_init import ADMIN_ID


router = Router()


@router.message(Command(commands=['admin']), F.from_user.id==ADMIN_ID)
async def admin_menu(message: Message, state: FSMContext):
    await state.set_state(FSM_bot.admin_menu)
    keyboard = await KeyboardFactory.get_markup(1, button_text['exit'], resize=True, persistent=True)
    await message.answer(text='⚠️ Включён режим администратора.', reply_markup=keyboard)


@router.message(F.text=='Выход', StateFilter(FSM_bot.admin_menu))
async def admin_menu(message: Message, state: FSMContext):
    await state.set_state(FSM_bot.user_menu)
    await message.answer(text=f'Введите команду /start для работы как обычный пользователь')


@router.callback_query(F.data=='accept', StateFilter(FSM_bot.admin_menu))
async def reg_cancel_inline(callback: CallbackQuery):
    await callback.message.edit_text(callback.message.text + '\nПринято ✅')


@router.callback_query(F.data=='cancel', StateFilter(FSM_bot.admin_menu))
async def reg_cancel_inline(callback: CallbackQuery):
    await callback.message.edit_text(callback.message.text + '\nОтменено ❌')
