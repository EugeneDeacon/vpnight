from typing import TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import AsyncSessionLocal

TRepo = TypeVar("TRepo")

class BaseService(Generic[TRepo]):
    """ Базовый сервис """

    _repo_class: type

    def __init__(self, session: AsyncSession | None = None):
        self._external_session = session
        self.session: AsyncSession | None = None
        self.repo: TRepo | None = None

    async def __aenter__(self):
        if self._external_session:
            self.session = self._external_session
        else:
            self.session = AsyncSessionLocal()
        assert self._repo_class
        self.repo = self._repo_class(session=self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._external_session and self.session:
            await self.session.close()
