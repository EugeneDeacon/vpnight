from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings:
    bot_token: str
    bot_url: str
    marzban_url: str
    marzban_login: str
    marzban_password: str
    gotify_url: str
    gotify_token: str
    price_1: int
    price_3: int
    database_url: str

def load_settings() -> Settings:
    return Settings(
        bot_token = os.getenv("BOT_TOKEN", ""),
        bot_url = os.getenv("BOT_URL", ""),
        marzban_url = os.getenv("MARZBAN_URL", ""),
        marzban_login = os.getenv("MARZBAN_LOGIN", ""),
        marzban_password = os.getenv("MARZBAN_PASSWORD", ""),
        gotify_url = os.getenv("GOTIFY_URL", ""),
        gotify_token = os.getenv("GOTIFY_TOKEN", ""),
        price_1 = int(os.getenv("PRICE_1", "160")),
        price_3 = int(os.getenv("PRICE_3", "410")),
        database_url = os.getenv("DATABASE_URL", ""),

    )
