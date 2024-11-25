import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram import types

from utils.config import BOT_KEY
from utils.logger.logger import BotLogger
from handlers import (
    start
)

# uncomment lines after fill database data in the .env
# from middlewares.user_ban import CheckUserWasBannedMiddleware

bot = Bot(token=BOT_KEY)
dp = Dispatcher()


async def bot_task(bot: bot, dp: Dispatcher):
    try:
        # uncomment lines after fill database data in the .env
        # from utils.db.models import init_db
        # await init_db()

        dp.include_routers(
            start.router
        )
        # uncomment lines after fill database data in the .env
        # dp.message.middleware(CheckUserWasBannedMiddleware())
        
        await BotLogger().info('✅ Bot started', send_alert=True)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, polling_timeout=11)
    except KeyboardInterrupt:
        await BotLogger().info(message='Bot manually stopped', send_alert=True)
    finally:
        await BotLogger().info(message='🏁 Bot stopped', send_alert=True)


async def additional_tasks(bot, dp):
    scheduler = AsyncIOScheduler()
    # Example
    # scheduler.add_job('cron', hour='*', minute=0)

    scheduler.start()


async def main(bot: bot, dp: Dispatcher):
    task1 = asyncio.create_task(bot_task(bot=bot, dp=dp))
    task2 = asyncio.create_task(additional_tasks(bot=bot, dp=dp))
    await asyncio.gather(task1, task2)
    

if __name__ == "__main__":
    try:
        asyncio.run(main(bot=bot, dp=dp))
    except asyncio.exceptions.CancelledError:
        pass
