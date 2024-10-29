from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(messange):
    await messange.answer("Привет! Я бот помогающий твоему здоровью.")


@dp.message_handler(text="Calories")
async def set_age(messange):
    await messange.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(messange, state):
    await state.update_data(first=messange.text)
    await messange.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(messange, state):
    await state.update_data(second=messange.text)
    await messange.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_colories(messange, state):
    await state.update_data(third=messange.text)
    data = await state.get_data()
    calc_colories = 10 * int(data['first']) + 6.25 * int(data['second']) + 5 * int(data['third'])
    await messange.answer(f"Ваша норма калорий: {calc_colories}")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

