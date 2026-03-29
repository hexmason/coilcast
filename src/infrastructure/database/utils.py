from infrastructure.db.base import engine, Base
from infrastructure.models import *


async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
