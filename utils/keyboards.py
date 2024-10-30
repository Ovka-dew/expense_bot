from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

categories = {
    "🍔 Еда": ["🍔 Фастфуд", "🍭 Сладкое", "🏡 Домой", "🥤 Напитки"],
    "💀 Привычки": ["🚬 Курение", "🍷 Алкоголь", "🥦 Шпек"],
    "🎁 Другое": ["❓ Неизвестное", "🛴 Транспорт"]
}

def get_categories_keyboard(callback_prefix="category"):
    buttons = [
        [InlineKeyboardButton(text=category, callback_data=f"{callback_prefix}:{category}")]
        for category in categories.keys()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_subcategories_keyboard(category):
    buttons = [
        [InlineKeyboardButton(text=subcategory, callback_data=f"subcategory:{subcategory}")]
        for subcategory in categories.get(category, [])
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)