from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, TypeVar

T = TypeVar("T")

class IRepository(ABC, Generic[T]):
    """
    Интерфейс репозитория для модели T.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def get_all(self, search: str | None, offset: int, limit: int) -> list[T] | None:
        ...

    async def get_by_id(self, id: int) -> T | None:
        ...

    @abstractmethod
    async def add(self, obj: dict) -> T:
        ...
