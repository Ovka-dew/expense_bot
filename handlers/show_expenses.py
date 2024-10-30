from aiogram import Router, types
from aiogram.filters import Command
from database import get_expenses_by_date
from datetime import datetime, timedelta

router = Router()

@router.message(Command("show_today"))
async def show_today_expenses(message: types.Message):
    today = datetime.now().strftime("%Y-%m-%d")
    expenses = await get_expenses_by_date(today, today)
    if expenses:
        response = "Расходы за сегодня:\n" + "\n".join([f"{e[1]} - {e[3]} pln." for e in expenses])
    else:
        response = "За сегодня расходов нет."
    await message.answer(response)

@router.message(Command("show_month"))
async def show_month_expenses(message: types.Message):
    today = datetime.now()
    start_of_month = today.replace(day=1).strftime("%Y-%m-%d")
    expenses = await get_expenses_by_date(start_of_month, today.strftime("%Y-%m-%d"))
    if expenses:
        response = "Расходы за текущий месяц:\n" + "\n".join([f"{e[0]} - {e[1]} - {e[3]} pln." for e in expenses])
    else:
        response = "За текущий месяц расходов нет."
    await message.answer(response)