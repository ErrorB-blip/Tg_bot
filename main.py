from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from core.handlers.basic import get_start
import asyncio
import logging
from core.settings import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers import apsched
from datetime import datetime, timedelta
from core.handlers import registration
from core.utils.statesform import StepsForm
async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')

async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    dp = Dispatcher()
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode='HTML'))
    dp.message.register(registration.get_form, Command= 'reg')
    dp.message.register(registration.get_name, StepsForm.GET_NAME)
    dp.message.register(registration.get_last_name, StepsForm.GET_LAST_NAME)
    dp.message.register(registration.get_day, StepsForm.GET_DAY)
    dp.message.register(registration.get_month, StepsForm.GET_MONTH)

    scheduler = AsyncIOScheduler(timezone= "Europe/Moscow")
    scheduler.add_job(apsched.send_message_cron, trigger='cron', hour=datetime.now().hour ,
                      minute=datetime.now().minute + 1, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.start()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())