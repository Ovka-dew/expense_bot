from aiogram import Router, types
from aiogram.filters import Command
from database import execute_query
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Create confirmation keyboards
def get_confirmation_keyboard(action: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data=f"confirm_{action}"),
            InlineKeyboardButton(text="Нет", callback_data="cancel_delete")
        ]
    ])

@router.message(Command("delete_today"))
async def delete_today_prompt(message: types.Message):
    """Ask for confirmation before deleting today's expenses"""
    await message.answer(
        "Вы уверены, что хотите удалить все расходы за сегодня?",
        reply_markup=get_confirmation_keyboard("today")
    )

@router.message(Command("delete_month"))
async def delete_month_prompt(message: types.Message):
    """Ask for confirmation before deleting month's expenses"""
    await message.answer(
        "Вы уверены, что хотите удалить все расходы за текущий месяц?",
        reply_markup=get_confirmation_keyboard("month")
    )

@router.callback_query(lambda c: c.data == "confirm_today")
async def delete_today_expenses(callback: types.CallbackQuery):
    """Handle confirmation for deleting today's expenses"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        query = "DELETE FROM expenses WHERE date = ?"
        await execute_query(query, (today,))
        await callback.message.edit_text("Расходы за сегодня успешно удалены.")
    except Exception as e:
        await callback.message.edit_text("Произошла ошибка при удалении расходов.")
    finally:
        await callback.answer()

@router.callback_query(lambda c: c.data == "confirm_month")
async def delete_month_expenses(callback: types.CallbackQuery):
    """Handle confirmation for deleting month's expenses"""
    try:
        today = datetime.now()
        start_of_month = today.replace(day=1).strftime("%Y-%m-%d")
        query = "DELETE FROM expenses WHERE date BETWEEN ? AND ?"
        await execute_query(query, (start_of_month, today.strftime("%Y-%m-%d")))
        await callback.message.edit_text("Расходы за текущий месяц успешно удалены.")
    except Exception as e:
        await callback.message.edit_text("Произошла ошибка при удалении расходов.")
    finally:
        await callback.answer()

@router.callback_query(lambda c: c.data == "cancel_delete")
async def cancel_delete(callback: types.CallbackQuery):
    """Handle cancellation of delete operation"""
    await callback.message.edit_text("Операция удаления отменена.")
    await callback.answer()