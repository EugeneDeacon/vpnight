from datetime import datetime, timedelta, timezone

from marzban import ProxySettings, UserCreate
from marzban.models import UserModify, UserResponse as MarzbanUser

from src.services.base import BaseMarzbanService


class MarzbanService(BaseMarzbanService):
    """Сервис по работе с Marzban API"""


    async def create_user(self, tg_id: int) -> MarzbanUser | None:
        """Создание пользователя в Marzban"""

        if not self.api or not self.token:
            raise RuntimeError("Сервис не инициализирован")

        expire_ts = int((datetime.now(timezone.utc) + timedelta(days=3)).timestamp())

        new_user = UserCreate(
            username=str(tg_id),
            proxies={
                "vless": ProxySettings(flow="xtls-rprx-vision")
            },
            inbounds={
                "vless": ["VLESS TCP REALITY"]
            },
            expire=expire_ts
        )

        added_user: MarzbanUser | None = await self.api.add_user(
            user=new_user,
            token=self.token.access_token
        )

        if not added_user:
            return None

        return added_user

    async def get_user(self, tg_id: int) -> MarzbanUser | None:
        """Находит пользователя в Marzban по tg_id"""

        if not self.api or not self.token:
            raise RuntimeError("Сервис не инициализирован")

        user: MarzbanUser | None = await self.api.get_user(username=str(tg_id), token=self.token.access_token)

        if not user:
            return None

        return user

    async def update_expire(self, tg_id: int, new_expire: int) -> bool:
        """Обновляет время истечения подписки пользователя"""

        if not self.api or not self.token:
            raise RuntimeError("Сервис не инициализирован")

        user: MarzbanUser | None = await self.api.get_user(username=str(tg_id), token=self.token.access_token)

        if not user:
            return False

        modified_user = await self.api.modify_user(
            username=str(tg_id),
            user=UserModify(expire=new_expire),
            token=self.token.access_token
        )

        if not modified_user:
            return False

        return True
