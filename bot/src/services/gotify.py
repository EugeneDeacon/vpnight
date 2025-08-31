import aiohttp

from src.services.base import BaseGotifyService
from config import load_settings

class GotifyService(BaseGotifyService):

    async def send_message(self, message: str, title: str = "Bot", priority: int = 5):
        """
        Отправка уведомления в Gotify.
        priority: 0-10 (чем выше, тем важнее)
        """
        if not self.session or not self.base_url:
            raise RuntimeError("Gotify service is not initialized")

        url = f"{self.base_url}/message"
        payload = {
            "title": title,
            "message": message,
            "priority": priority
        }

        async with self.session.post(url, json=payload) as resp:
            if resp.status != 200:
                text = await resp.text()
                print(text)
                raise RuntimeError(f"Gotify error {resp.status}: {text}")
            return await resp.json()
