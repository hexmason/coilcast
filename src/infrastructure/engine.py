from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from application.config.settings import settings


engine = create_async_engine(
    url=str(settings.DATABASE_URI),
    echo=settings.DEBUG_MODE
)

AsyncSessionLocal = async_sessionmaker(
    expire_on_commit=False,
    autoflush=False,
    bind=engine
)
