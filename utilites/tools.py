import re
from aiogram.fsm.context import FSMContext
from text.bot_reply import reserve_message
from bot_init import bot_db

class BasicTools:

    @staticmethod
    async def clear_phone_number(message: str) -> str:
        return re.sub(r'[\W_]', '', message)


    @staticmethod
    async def check_user_name(message: str) -> bool:
        return bool(re.fullmatch(r'^[а-яА-ЯёЁ]+$', message))


    @staticmethod
    async def prepare_to_admin_message(user_id: int, state_data: FSMContext) -> str:
        reserve_data = await state_data.get_data()
        user_info = await bot_db.get_user_data(user_id)
        return reserve_message.format(user_info['name'], 
                                      user_info['username'], 
                                      user_info['phone'], 
                                      reserve_data.get('date'), 
                                      reserve_data.get('time')
                                      )
    

    @staticmethod
    async def check_referer(payload: str) -> bool:
        if payload.isdigit():
            if bot_db.get_user_id(int(payload)):
                return True
            else:
                return False
        else:
            return False