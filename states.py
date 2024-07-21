from aiogram.dispatcher.filters.state import StatesGroup, State

class adm_states(StatesGroup):
    get_sum_id = State()
    new_give_money = State()
    get_shop_acc = State()
    input_new_geo_sum = State()
    new_input_new_geo_sum = State()

class user_states(StatesGroup):
    for_maill = State()

    proxy = State()
    new_acc_buy = State()