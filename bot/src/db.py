from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import load_settings

cfg = load_settings()

engine = create_async_engine(
    cfg.database_url,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

async def new_session() -> AsyncSession:
    """
    Возвращает сессию.
    """
    return AsyncSessionLocal()
