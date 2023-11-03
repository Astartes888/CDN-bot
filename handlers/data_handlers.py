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
from buttons.buttons_factory import KeyboardFactory
from text.button_text import menu_text
from bot_init import bot_db, api, ORG_ID


router = Router()


@router.message(StateFilter(default_state), F.content_type == ContentType.WEB_APP_DATA)
async def get_app_data(message: Message, state: FSMContext):
    data = json.loads(message.web_app_data.data)
    referrer_data = await state.get_data()
    referrer_id = referrer_data.get('referrer_id')
    try:
        await bot_db.set_user_data(message.from_user.id, 
                             message.chat.id, 
                             f'@{message.from_user.username}' if message.from_user.username else f'tg://openmessage?user_id={message.from_user.id}', 
                             data['number'], 
                             data['name']
                             )
        if referrer_id:
            referrer_info = await bot_db.get_user_data(int(referrer_id))
            await api.refill_balance(organization_id=ORG_ID, customer_id=referrer_info['customer_id'], wallet_id=referrer_info['wallet_id'], sum=500)
        customer_id = await api.customer_create_or_update(ORG_ID, phone=data['number'], name=data['name'])
        await bot_db.update_customer_id(message.from_user.id, customer_id.id)
        wallet_id = await api.customer_info(ORG_ID, type='id', identifier=customer_id.id)
        await bot_db.update_wallet_id(message.from_user.id, wallet_id.wallet_balances[0].id)
        
        await state.set_state(FSM_bot.user_menu)
        keyboard = await KeyboardFactory.get_custom_markup([2, 2, 1], menu_text, resize=True, persistent=True)
        await message.answer(bot_text['greetings'], reply_markup=keyboard)
        
    except Exception as e:
        print(e)
