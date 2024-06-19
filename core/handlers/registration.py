from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.utils.statesform import StepsForm
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers.apsched import send_message_cron
from datetime import datetime, timedelta
from aiogram import Bot

async def get_form(message: Message, state: FSMContext) :
    await message.answer(f'{message.from_user.first_name}, Начинаем регистрацию, введите имя')
    await state.set_state(StepsForm.GET_NAME)

async def get_name(message: Message, state: FSMContext):
    await message.answer(f'Ваше имя:\r\n{message.text}\r\n, Введите фамилию')
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_LAST_NAME)

async def get_last_name(message: Message, state: FSMContext):
    await message.answer(f'Ваша фамилия:\r\n{message.text}\r\n, введите день рождения')
    await state.update_data(last_name=message.text)
    await state.set_state(StepsForm.GET_DAY)

async def get_day(message: Message, state: FSMContext):
    await message.answer(f'Ваш день рождения:\r\n{message.text}\r\n, введите месяц рождения')
    await state.update_data(day=message.text)
    await state.set_state(StepsForm.GET_MONTH)

async def get_month(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler):
    await message.answer(f'Месяц рождения:\r\n{message.text}\r\n')
    context_data = await state.get_data()
    await message.answer(f'Сохраненные данные\r\n{str(context_data)}')
    name = context_data.get('name')
    last_name = context_data.get('last_name')
    day = context_data.get('day')
    data_user  = (f'Ваши данные \r\n '\
                  f'Имя {name}'\ 
                  f'Фамилия {last_name}'\ 
                  f'Дата рождения {day}.{message.text}')
    await message.answer(data_user)
    await state.clear()






