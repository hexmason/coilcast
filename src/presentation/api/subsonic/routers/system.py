from fastapi import APIRouter, Response, Query, Depends

# from presentation.schemas.responses import SubsonicResponseFactory
from presentation.api.subsonic.routers.dependencies import SubsonicAuthContext
from presentation.api.subsonic.response_builder import (
    build_error_response,
    build_response,
)
from presentation.api.subsonic.routers.dependencies import (
    SubsonicAuthContext,
    subsonic_auth,
)

system_router = APIRouter()


@system_router.get("/ping")
async def ping(
    auth: SubsonicAuthContext = Depends(subsonic_auth), f: str = Query("json")
) -> Response:
    if auth and f:
        return build_response({}, f)
    else:
        return build_error_response(10, f)  # add verification versions


@system_router.get("/getLicense")
async def get_license(
    auth: SubsonicAuthContext = Depends(subsonic_auth), f: str = Query("json")
) -> Response:
    data = {"license": {"valid": True}}  # add other parameters
    return build_response(data, f)
