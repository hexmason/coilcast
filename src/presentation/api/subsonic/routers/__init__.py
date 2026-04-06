from fastapi import APIRouter

from presentation.api.subsonic.routers.system import system_router
from presentation.api.subsonic.routers.browsing import browsing_router
from presentation.api.subsonic.routers.media_retrieval import media_retrieval_router
from presentation.api.subsonic.routers.media_library_scanning import (
    media_library_scanning_router,
)

subsonic_router = APIRouter()

subsonic_router.include_router(system_router)
subsonic_router.include_router(browsing_router)
subsonic_router.include_router(media_retrieval_router)
subsonic_router.include_router(media_library_scanning_router)
