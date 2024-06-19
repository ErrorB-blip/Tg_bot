import asyncpg
import asyncio
from core.handlers import registration
from aiogram.types import Message
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
async def create_pool():
    return await asyncpg.create_pool(
        user='your_username',
        password='your_password',
        database='your_database',
        host='your_host'
    )


async def add_user_to_db(pool, name, last_name, birthday):
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO users (name, last_name, birthday) VALUES ($1, $2, $3)",
            name, last_name, birthday
        )


async def get_month(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler, pool):

    context_data = await state.get_data()
    name = context_data.get('name')
    last_name = context_data.get('last_name')
    day = context_data.get('day')
    month = message.text


    await add_user_to_db(pool, name, last_name, f"{day}.{month}")


    await state.clear()


pool = asyncio.get_event_loop().run_until_complete(create_pool())
