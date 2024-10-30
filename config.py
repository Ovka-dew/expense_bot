import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_TOKEN: str = os.getenv("API_TOKEN", "")
    DB_NAME: str = os.getenv("DB_NAME", "expenses.db")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

config = Config()