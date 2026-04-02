from infrastructure.database.engine import engine
from infrastructure.database.models import *
from infrastructure.database.models.base import Base


async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
