import asyncio
from fastapi import FastAPI, Header, Request
from uvicorn import Config, Server
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from src.constants import Texts
from config import load_settings
from src.services.notification import NotificationService
from src.handlers import register_handlers

# =========================
# Настройка бота и dp
# =========================
cfg = load_settings()

bot = Bot(
    token=cfg.bot_token,
    default=DefaultBotProperties(parse_mode="Markdown")
)

dp = Dispatcher(storage=MemoryStorage())
dp["notifications"] = NotificationService(bot)

register_handlers(dp)

# =========================
# FastAPI
# =========================
app = FastAPI()

def day_plural(n: int) -> str:
    n = abs(n) % 100
    n1 = n % 10
    if 11 <= n <= 19:
        return "дней"
    if n1 == 1:
        return "день"
    if 2 <= n1 <= 4:
        return "дня"
    return "дней"

@app.post("/webhook")
async def webhook_endpoint(request: Request, x_webhook_secret: str | None = Header(None)):
    event = await request.json()
    if event is None:
        return {"status": "error", "message": "Invalid data"}
    if event[0].get("action") != "reached_days_left":
        return {"status": "ok"}
    print(event)
    username = event[0].get("username")
    days_left = event[1].get("days_left")

    text = Texts.REACHED_DAYS.format(
        days=days_left,
        name_day=day_plural(days_left)
    )
    notifications: NotificationService = dp["notifications"]
    await notifications.send_message(chat_id=username, text=text)

    return {"status": "ok"}


# =========================
# Основная функция
# =========================
async def main():
    print("Bot + FastAPI running...")

    # uvicorn конфигурация
    config = Config(app=app, host="0.0.0.0", port=8000, log_level="info")
    server = Server(config=config)

    # запускаем бота и FastAPI параллельно
    await asyncio.gather(
        dp.start_polling(bot),
        server.serve()
    )


if __name__ == "__main__":
    asyncio.run(main())
