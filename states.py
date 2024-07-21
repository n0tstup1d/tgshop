from aiogram.dispatcher.filters.state import StatesGroup, State

class adm_states(StatesGroup):
    get_sum_id = State()
    new_give_money = State()

class user_states(StatesGroup):
    for_maill = State()

    proxy = State()