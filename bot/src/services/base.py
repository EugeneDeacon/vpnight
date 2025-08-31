from typing import Optional, TypeVar, Generic
from marzban import MarzbanAPI, Token
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from config import load_settings
from src.db import AsyncSessionLocal

TRepo = TypeVar("TRepo")

class BaseService(Generic[TRepo]):
    """ Базовый сервис для моделей БД"""

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



class BaseMarzbanService:
    """Базовый сервис для Marzban"""

    def __init__(self):
        self.api: MarzbanAPI | None = None
        self.token: Token | None = None

    async def __aenter__(self):
        cfg = load_settings()
        self.api = MarzbanAPI(base_url=cfg.marzban_url)
        self.token = await self.api.get_token(
            username=cfg.marzban_login,
            password=cfg.marzban_password
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class BaseGotifyService:
    """Базовый сервис для Gotify"""

    def __init__(self):
        self.base_url: Optional[str] = None
        self.token: Optional[str] = None
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        cfg = load_settings()
        self.base_url = cfg.gotify_url.rstrip("/")
        self.token = cfg.gotify_token

        self.session = aiohttp.ClientSession(
            headers={"X-Gotify-Key": self.token}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
