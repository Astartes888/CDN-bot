from aiogram import Router
from aiogram import F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import CommandStart, StateFilter, or_f
#from aiogram.methods.send_chat_action import SendChatAction
from aiogram.types.web_app_info import WebAppInfo
from buttons.buttons_factory import KeyboardFabric
from text.bot_reply import bot_text, promo_text
from text.button_text import button_text, menu_text, web_app_reg, bonus_menu_text   
from states.bot_states import FSM_bot


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def user_registration(message: Message):
    #web_app = WebAppInfo(url=web_app_reg)
    keyboard = await KeyboardFabric.get_markup(1, button_text['authorize'], resize=True) #web_app=web_app)
    await message.answer(bot_text['start_command'], reply_markup=keyboard)


@router.message(CommandStart(), StateFilter(FSM_bot.user_menu))
async def user_registration(message: Message):
    keyboard = await KeyboardFabric.get_custom_markup([2, 2, 1], menu_text, resize=True, )
    await message.answer(bot_text['greetings'], reply_markup=keyboard)


@router.message(F.text==button_text['back'], StateFilter(FSM_bot.date_reserve))
async def feedback(message: Message, state: FSMContext):
    await state.set_state(FSM_bot.user_menu)
    keyboard = await KeyboardFabric.get_custom_markup([2, 2, 1], menu_text, resize=True, )
    await message.answer(bot_text['greetings'], reply_markup=keyboard)


@router.message(F.text==button_text['back'], StateFilter(FSM_bot.time_reserve)) 
async def feedback(message: Message, state: FSMContext):
    await state.set_state(FSM_bot.user_menu)
    keyboard = await KeyboardFabric.get_custom_markup([2, 2, 1], menu_text, resize=True)
    await message.answer(bot_text['greetings'], reply_markup=keyboard)


@router.message(F.text==button_text['back'], StateFilter(FSM_bot.bonus_menu))
async def feedback(message: Message, state: FSMContext):
    await state.set_state(FSM_bot.user_menu)
    keyboard = await KeyboardFabric.get_custom_markup([2, 2, 1], menu_text, resize=True)
    await message.answer(bot_text['greetings'], reply_markup=keyboard)


@router.message(F.text=='Начать работу', StateFilter(default_state)) # Заглушка первой кнопки
async def greetings_user(message: Message, state: FSMContext):
    await state.set_state(FSM_bot.user_menu)
    keyboard = await KeyboardFabric.get_custom_markup([2, 2, 1], menu_text, resize=True)
    await message.answer(bot_text['greetings'], reply_markup=keyboard)


@router.message(F.text=='Спец предложения', StateFilter(FSM_bot.user_menu))
async def promo(message: Message):
    await message.answer(promo_text)
        

@router.message(F.text=='Контакты', StateFilter(FSM_bot.user_menu))
async def contacts(message: Message):
    await message.answer_photo(photo=FSInputFile('/City_project/photo/city_1.jpg'), caption=bot_text['adress'])


@router.message(F.text=='Бронь', StateFilter(FSM_bot.user_menu))
async def start_reserve(message: Message, state: FSMContext):
    await state.set_state(FSM_bot.date_reserve)
    keyboard = await KeyboardFabric.get_markup(1, button_text['back'], resize=True)    
    await message.answer(bot_text['answers'], reply_markup=keyboard)
    await message.answer(bot_text['answer_date'])


@router.message(F.text, StateFilter(FSM_bot.date_reserve))
async def ask_time_reserve(message: Message, state: FSMContext):
    # <- тут валидация введёной даты брони
    await state.set_state(FSM_bot.time_reserve)
    await state.update_data(date=message.text)
    keyboard = await KeyboardFabric.get_markup(1, button_text['back'], resize=True)    
    await message.answer(bot_text['answer_time'], reply_markup=keyboard)


@router.message(F.text, StateFilter(FSM_bot.time_reserve))
async def done_reserve(message: Message, state: FSMContext):
    # <- тут валидация введёного времени брони
    await state.update_data(time=message.text)
    await state.set_state(FSM_bot.user_menu)
    keyboard = await KeyboardFabric.get_custom_markup([2, 2, 1], menu_text, resize=True)    
    await message.answer(bot_text['call_you'], reply_markup=keyboard)


@router.message(F.text=='Бонусы', StateFilter(FSM_bot.user_menu))
async def bonus(message: Message, state: FSMContext):    
    await state.set_state(FSM_bot.bonus_menu)
    keyboard = await KeyboardFabric.get_markup(2, *bonus_menu_text, resize=True)
    await message.answer(bot_text['bonus_menu'], reply_markup=keyboard)
    
    
@router.message(F.text==bonus_menu_text[0], StateFilter(FSM_bot.bonus_menu))
async def bonus(message: Message):    
    keyboard = await KeyboardFabric.get_markup(2, *bonus_menu_text, resize=True)
    await message.answer('На вашем счете 0 бонусных рублей.\nВаша скидка {bonus_level}%\nПриглашайте больше друзей, учавствуйте в акциях и зарабатывайте больше бонусных рублей!', reply_markup=keyboard)  
    

@router.message(F.text==bonus_menu_text[1], StateFilter(FSM_bot.bonus_menu))
async def bonus(message: Message):    
    keyboard = await KeyboardFabric.get_markup(2, *bonus_menu_text, resize=True)
    await message.answer('Приглашайте друзей и получайте 500 бонусных рублей на счет!\nВаша ссылка для приглашения: {url}', reply_markup=keyboard)  


# @router.callback_query(F.text == 'Забронировать стол', StateFilter(FSM_bot.user_menu))
# async def inline_menu(callback: CallbackQuery, state: FSMContext):
#     await callback.answer()