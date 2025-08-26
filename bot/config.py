from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings:
    bot_token: str
    database_url: str

def load_settings() -> Settings:
    return Settings(
        bot_token = os.getenv("BOT_TOKEN", ""),
        database_url = os.getenv("DATABASE_URL", ""),
    )
