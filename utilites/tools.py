import re
from aiogram.fsm.context import FSMContext

class BasicTools:

    @staticmethod
    async def check_phone_number(message : str) -> bool:
        if message in "Нет номера":
            return await True
        else:
            clear_number = await re.sub(r'[\W_]', '', message)
            if len(clear_number) >= 10 and len(clear_number) <= 11:
                return await clear_number.isdigit()
            else:
                return await False

    # @staticmethod
    # def ending_of_word(cls, ammount) :
    #     f1 = lambda a: (a%100)//10 != 1 and a%10 == 1
    #     f2 = lambda a: (a%100)//10 != 1 and a%10 in [2,3,4]
    #     return "обращение" if f1(ammount) else  "обращения" if f2(ammount) else "обращений"

    async def prepare_to_admin_message(state_data: FSMContext):
        pass