from src.repositories.users import UserRepository
from src.models.users import User
from typing import Dict

from src.services.base import BaseService

class UserService(BaseService[UserRepository]):
    _repo_class = UserRepository

    async def register(self, user_info: Dict) -> User:
        assert self.repo

        user_id: int | None = user_info.get("id")
        if user_id is None:
            raise ValueError("User ID is required")

        existing_user = await self.repo.get_by_id(user_id)

        if existing_user:
            return existing_user

        return await self.repo.add(user_info)
