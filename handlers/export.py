import csv
import tempfile
import os
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from database import get_expenses_by_date
from datetime import datetime

router = Router()

@router.message(Command("export"))
async def export_expenses(message: types.Message):
    start_date = datetime.now().replace(day=1).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")

    expenses = await get_expenses_by_date(start_date, end_date)

    if not expenses:
        await message.answer("Нет данных для экспорта за текущий месяц.")
        return

    with tempfile.NamedTemporaryFile(mode="w+", newline="", encoding="utf-8", suffix=".csv", delete=False) as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(["Дата", "Категория", "Подкатегория", "Сумма"])
        for expense in expenses:
            writer.writerow(expense)
        temp_file_path = temp_file.name

    await message.answer_document(FSInputFile(temp_file_path))
    os.unlink(temp_file_path)