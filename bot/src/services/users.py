from src.services.marzban import MarzbanService
from src.repositories.users import UserRepository
from src.services.gotify import GotifyService
from src.models.users import User
from typing import Dict

from src.services.base import BaseService

class UserService(BaseService[UserRepository]):
    _repo_class = UserRepository

    async def get_by_id(self, id: int) -> User | None:
        """Ищет пользователя в базе данных по ID"""
        assert self.repo

        if id is None:
            raise ValueError("User ID is required")

        existing_user = await self.repo.get_by_id(id)

        if not existing_user:
            raise ValueError("User not found")

        return existing_user

    async def register(self, user_info: Dict) -> User:
        """Создает нового пользователя в базе данных и в Marzban"""
        assert self.repo

        user_id: int | None = user_info.get("id")
        if user_id is None:
            raise ValueError("User ID is required")

        existing_user = await self.repo.get_by_id(user_id)

        if existing_user:
            return existing_user


        new_user = await self.repo.add(user_info)

        async with MarzbanService() as service:
            marzban_user = await service.create_user(new_user.id)

        if not marzban_user:
            raise ValueError("Failed to create user in Marzban")

        async with GotifyService() as service:
            user_identifier = new_user.username if new_user.username is not None else new_user.id
            gotify_user = await service.send_message(message=f"Новый пользователь {user_identifier}", title="Новый пользователь", priority=5)

        return new_user

    async def update_user(self, id: int, fields: dict) -> User:
            """Обновляет пользователя"""
            assert self.repo
            user = await self.repo.update(id, fields)
            if not user:
                raise ValueError("User not found")
            return user
