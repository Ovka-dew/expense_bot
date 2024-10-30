from aiogram import Bot
from aiogram.types import BotCommand

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начало работы"),
        BotCommand(command="/add_expense", description="Добавить расход"),
        BotCommand(command="/show_today", description="Показать расходы за сегодня"),
        BotCommand(command="/show_month", description="Показать расходы за месяц"),
        BotCommand(command="/delete_today", description="Удалить записи за сегодня"),
        BotCommand(command="/delete_month", description="Удалить записи за месяц"),
        BotCommand(command="/export", description="Выгрузка данных за месяц")

    ]
    await bot.set_my_commands(commands)