import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import load_settings
from src.handlers import register_handlers

async def main():
    cfg = load_settings()

    bot = Bot(
        token=cfg.bot_token,
        default=DefaultBotProperties(parse_mode="Markdown")
    )

    dp = Dispatcher(storage=MemoryStorage())

    register_handlers(dp)

    print("Bot is running...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
