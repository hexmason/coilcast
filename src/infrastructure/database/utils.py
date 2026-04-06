from infrastructure.database.engine import engine, AsyncSessionLocal
from infrastructure.database.models import *
from infrastructure.database.models.base import Base


async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
