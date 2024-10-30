from aiogram import Router
from . import start, add_expense, show_expenses, delete_expenses, export

def register_handlers(router: Router):
    router.include_router(start.router)
    router.include_router(add_expense.router)
    router.include_router(show_expenses.router)
    router.include_router(delete_expenses.router)
    router.include_router(export.router)