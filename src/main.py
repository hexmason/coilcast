import uvicorn
from fastapi import Depends, FastAPI

from application.config.settings import Settings
from application.services.library_scanner import LibraryScannerService
from application.services.library_sync import LibrarySyncService
from infrastructure.database.utils import init_database
from infrastructure.database.unit_of_work import UnitOfWork
from infrastructure.providers.mutagen_metadata import MutagenMetadataProvider
from presentation.api.subsonic.routers import subsonic_router
from presentation.api.subsonic.routers.dependencies import get_uow

settings = Settings()
app = FastAPI()
app.include_router(subsonic_router, prefix="/rest", tags=["rest"])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=settings.HTTP_PORT)


@app.post("/setup_database")
async def setup_db(uow: UnitOfWork = Depends(get_uow)):
    await init_database()
    scanner_service = LibraryScannerService(settings.MUSIC_FOLDER)
    metadata_provider = MutagenMetadataProvider()
    sync_service = LibrarySyncService(scanner_service, metadata_provider, uow)
    await sync_service.sync()
    return {"status": "ok"}
