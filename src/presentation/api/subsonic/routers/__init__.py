from fastapi import APIRouter

from presentation.api.subsonic.routers.system import router as system_router

subsonic_router = APIRouter()

subsonic_router.include_router(system_router)
