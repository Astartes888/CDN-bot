import re
from aiogram.fsm.context import FSMContext
from text.bot_reply import reserve_message
from bot_init import bot_db

class BasicTools:

    @staticmethod
    async def check_phone_number(message: str) -> bool:
        if message in "Нет номера":
            return True
        else:
            clear_number = await re.sub(r'[\W_]', '', message)
            if len(clear_number) >= 10 and len(clear_number) <= 11:
                return clear_number.isdigit()
            else:
                return False

    # @staticmethod
    # def ending_of_word(cls, ammount) :
    #     f1 = lambda a: (a%100)//10 != 1 and a%10 == 1
    #     f2 = lambda a: (a%100)//10 != 1 and a%10 in [2,3,4]
    #     return "обращение" if f1(ammount) else  "обращения" if f2(ammount) else "обращений"

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