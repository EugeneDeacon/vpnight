from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from .base import IRepository
from src.models.users import User


class UserRepository(IRepository[User]):

    async def get_all(
        self,
        search: str | None = None,
        offset: int = 0,
        limit: int = 10
    ) -> list[User]:
        """Получение всех пользователей"""
        stmt = select(User)

        if search:
            stmt = stmt.where(
                (User.username.ilike(f"%{search}%")) |
                (User.first_name.ilike(f"%{search}%"))
            )

        stmt = stmt.offset(offset).limit(limit)

        res = await self.session.execute(stmt)
        return list(res.scalars().all())


    async def get_by_id(self, id: int) -> User | None:
        """Получение пользователя по id"""
        stmt = select(User).options(selectinload(User.referrals)).where(User.id == id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()


    async def add(self, obj: dict) -> User:
        """Создать нового пользователя"""
        user = User(**obj)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, id: int, fields: dict) -> User | None:
        """Обновление пользователя по ID"""
        stmt = update(User).where(User.id == id).values(**fields).returning(User)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one_or_none()
