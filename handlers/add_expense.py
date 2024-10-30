from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from utils.keyboards import get_categories_keyboard, get_subcategories_keyboard
from database import execute_query
from datetime import datetime
from logger import logger  # Импортируйте логгер

router = Router()


class ExpenseState(StatesGroup):
    waiting_for_amount = State()
    waiting_for_category = State()
    waiting_for_subcategory = State()
    waiting_for_sum_type = State()  # Добавлено для суммирования


@router.message(Command("add_expense"))
async def prompt_add_expense(message: types.Message, state: FSMContext):
    await message.answer("Введите сумму покупки в PLN:")
    await state.set_state(ExpenseState.waiting_for_amount)


@router.message(ExpenseState.waiting_for_amount)
async def get_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.replace(',', '.'))
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        await state.update_data(current_amount=amount)
        await message.answer("Выберите категорию:", reply_markup=get_categories_keyboard())
        await state.set_state(ExpenseState.waiting_for_category)
        logger.info(f"Сумма {amount} PLN введена пользователем {message.from_user.id}.")
    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму (положительное число).")


@router.callback_query(lambda c: c.data.startswith('category:'))
async def process_category_selection(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split(':')[1]
    await state.update_data(current_category=category)
    await callback.message.edit_text(f"Выберите подкатегорию для {category}:",
                                     reply_markup=get_subcategories_keyboard(category))
    await state.set_state(ExpenseState.waiting_for_subcategory)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith('subcategory:'))
async def process_subcategory_selection(callback: types.CallbackQuery, state: FSMContext):
    subcategory = callback.data.split(':')[1]
    user_data = await state.get_data()

    amount = user_data['current_amount']
    category = user_data['current_category']

    current_date = datetime.now().strftime("%Y-%m-%d")

    query = '''
    INSERT INTO expenses (date, category, subcategory, amount)
    VALUES (?, ?, ?, ?)
    '''
    await execute_query(query, (current_date, category, subcategory, amount))

    await callback.message.edit_text(
        f"Расход сохранен:\n"
        f"Сумма: {amount} PLN\n"
        f"Категория: {category}\n"
        f"Подкатегория: {subcategory}"
    )

    logger.info(f"Расход добавлен: {amount} PLN, категория: {category}, подкатегория: {subcategory}.")

    await state.clear()
    await callback.answer()