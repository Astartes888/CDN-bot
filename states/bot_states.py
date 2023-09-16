from aiogram.fsm.state import State, StatesGroup


class FSM_bot(StatesGroup):
    date_reserve = State()
    time_reserve = State()
    table_reserve = State()
    user_menu = State()
    bonus_menu = State()
    admin_menu = State()