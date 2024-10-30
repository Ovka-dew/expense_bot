import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from handlers import register_handlers
from utils.commands import set_bot_commands
from database import init_db

logging.basicConfig(level=logging.INFO if config.DEBUG else logging.WARNING)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=config.API_TOKEN)
    dp = Dispatcher()

    try:
        await init_db()
        register_handlers(dp)
        await set_bot_commands(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Произошла ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен.")