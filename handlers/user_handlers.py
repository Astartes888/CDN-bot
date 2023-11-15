from aiogram import Router
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import CommandStart, StateFilter, or_f, CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload
from buttons.buttons_factory import KeyboardFactory
from buttons.ready_keyboards import (generating_keyboard_menu, 
                                     generating_keyboard_with_contact, 
                                     generating_keyboard_bonus_menu)
from text.bot_reply import bot_text, promo_text
from text.button_text import button_text, bonus_menu_text, contact_photo_id
from states.bot_states import FSM_bot
from bot_init import bot, bot_db, api, logger, ORG_ID, ADMIN_ID
from utilites.tools import BasicTools


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def user_registration(message: Message, command: CommandObject, state: FSMContext): 
    keyboard = await KeyboardFactory.get_markup(1, button_text['authorize'], 
                                               resize=True,  
                                               persistent=True
                                               )
    # Если объект типа CommandObject имеет аругменты после команды /start, 
    # т.е. если зашли по ссылке с параметрами (по реферальной ссылке), то выполняются условия.
    if command.args:
        try:
            payload = decode_payload(command.args)
        except UnicodeDecodeError as err:
            await message.answer("Реферальная ссылка не действительна. Запросите новую или зарегистрируйтесь обычным способом через /start")
            logger.exception(f'Ошибка декодирования ссылки.\nПричина: {err}')
        if BasicTools.check_referer(payload):
            await state.update_data(referrer_id=str(payload))
            await message.answer(bot_text['start_command'], reply_markup=keyboard)
        else:
            await message.answer("Реферальная ссылка не действительна. Запросите новую или зарегистрируйтесь обычным способом через /start")
    else:
        await message.answer(bot_text['start_command'], reply_markup=keyboard)


@router.message(CommandStart(), or_f(StateFilter(FSM_bot.date_reserve), 
                                     StateFilter(FSM_bot.time_reserve), 
                                     StateFilter(FSM_bot.bonus_menu), 
                                     StateFilter(FSM_bot.user_menu)
                                     ))
async def user_registration(message: Message):
    keyboard = await generating_keyboard_menu()
    await message.answer(bot_text['greetings'], reply_markup=keyboard)


@router.message(F.text==button_text['back'], or_f(StateFilter(FSM_bot.fill_username), StateFilter(FSM_bot.get_contact)))
async def cancel_reg_process(message: Message, state: FSMContext):
    await state.clear()
    keyboard = await KeyboardFactory.get_markup(1, 'Начать работу', resize=True, persistent=True)
    await message.answer(bot_text['start_command'], reply_markup=keyboard)


@router.message(F.text==button_text['back'], or_f(StateFilter(FSM_bot.date_reserve), 
                                                  StateFilter(FSM_bot.time_reserve),
                                                  StateFilter(FSM_bot.bonus_menu),
                                                  ))
async def cancel_states(message: Message, state: FSMContext):
    await state.set_state(FSM_bot.user_menu)
    await state.set_data({})
    keyboard = await generating_keyboard_menu()
    await message.answer(bot_text['greetings'], reply_markup=keyboard)


@router.message(F.text==button_text['authorize'], StateFilter(default_state))
async def request_name(message: Message, state: FSMContext):
    await state.set_state(FSM_bot.fill_username)
    keyboard = await KeyboardFactory.get_markup(1, button_text['back'], resize=True, persistent=True)
    await message.answer(bot_text['name'], reply_markup=keyboard)


@router.message(F.text, StateFilter(FSM_bot.fill_username))
async def start_func(message: Message, state: FSMContext):
    check_result = await BasicTools.check_user_name(message.text)
    if not check_result:
        await message.answer(bot_text['wrong_name'])
        return
    await state.update_data(username=message.text.capitalize())
    await state.set_state(FSM_bot.get_contact)
    keyboard = await generating_keyboard_with_contact()
    await message.answer(bot_text['phone'], reply_markup=keyboard)


@router.message(F.text=='Акции', StateFilter(FSM_bot.user_menu))
async def promo(message: Message):
    await message.answer(promo_text)


@router.message(F.text=='Контакты', StateFilter(FSM_bot.user_menu))
async def contacts(message: Message):
    await message.answer_photo(photo=contact_photo_id, caption=bot_text['adress'])


@router.message(F.text=='Бронь', StateFilter(FSM_bot.user_menu))
async def start_reserve(message: Message, state: FSMContext):
    await state.set_state(FSM_bot.date_reserve)
    keyboard = await KeyboardFactory.get_markup(1, button_text['back'], resize=True, persistent=True)    
    await message.answer(bot_text['answers'], reply_markup=keyboard)
    await message.answer(bot_text['answer_date'])


@router.message(F.text, StateFilter(FSM_bot.date_reserve))
async def ask_time_reserve(message: Message, state: FSMContext):
    await state.set_state(FSM_bot.time_reserve)
    await state.update_data(date=message.text.lower())
    keyboard = await KeyboardFactory.get_markup(1, button_text['back'], resize=True, persistent=True)    
    await message.answer(bot_text['answer_time'], reply_markup=keyboard)


@router.message(F.text, StateFilter(FSM_bot.time_reserve))
async def done_reserve(message: Message, state: FSMContext):
    await state.update_data(time=message.text.lower())
    text = await BasicTools.prepare_to_admin_message(message.from_user.id, state)
    try:
        inline_keyboard = await KeyboardFactory.get_inline_markup(2, 'accept', 'cancel')
        await bot.send_message(chat_id=ADMIN_ID, text=text, reply_markup=inline_keyboard)
    except Exception as err:
        logger.exception(f'Не удалось отправить сообщение администратору.\nПричина: {err}')
    await state.set_data({})
    await state.set_state(FSM_bot.user_menu)
    keyboard = await generating_keyboard_menu()    
    await message.answer(bot_text['call_you'], reply_markup=keyboard)


@router.message(F.text=='Бонусы', StateFilter(FSM_bot.user_menu))
async def bonus(message: Message, state: FSMContext):    
    await state.set_state(FSM_bot.bonus_menu)
    keyboard = await generating_keyboard_bonus_menu()
    await message.answer(bot_text['bonus_menu'], reply_markup=keyboard)


@router.message(F.text==bonus_menu_text[0], StateFilter(FSM_bot.bonus_menu))
async def bonus(message: Message):    
    keyboard = await generating_keyboard_bonus_menu()
    user_info = await bot_db.get_user_data(message.from_user.id)
    wallet = await api.customer_info(organization_id=ORG_ID, type='id', identifier=user_info['customer_id'])
    wallet_balance = wallet.wallet_balances[0].balance
    await message.answer(f'На вашем счете {int(wallet_balance)} бонусных рублей.', reply_markup=keyboard)  


@router.message(F.text==bonus_menu_text[1], StateFilter(FSM_bot.bonus_menu))
async def bonus(message: Message):    
    keyboard = await generating_keyboard_bonus_menu()
    link = await create_start_link(bot, str(message.from_user.id), encode=True) # Создаём зашифрованную реферальную ссылку из id пользователя
    await message.answer(bot_text['referal_link'].format(link), reply_markup=keyboard)

