import aiosqlite
from config import config

async def init_db():
    async with aiosqlite.connect(config.DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                amount REAL NOT NULL CHECK(amount >= 0)
            )
        ''')
        await db.commit()

async def execute_query(query: str, parameters: tuple = ()) -> list:
    async with aiosqlite.connect(config.DB_NAME) as db:
        async with db.execute(query, parameters) as cursor:
            result = await cursor.fetchall()
        await db.commit()
    return result

async def get_expenses_by_date(start_date: str, end_date: str) -> list:
    query = '''
    SELECT date, category, subcategory, amount
    FROM expenses
    WHERE date BETWEEN ? AND ?
    '''
    return await execute_query(query, (start_date, end_date))