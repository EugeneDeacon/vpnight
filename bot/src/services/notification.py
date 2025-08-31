from aiogram import Bot


class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_message(self, chat_id: int, text: str):
        await self.bot.send_message(chat_id=chat_id, text=text)
