from fastapi import APIRouter, Response, Query, Depends
from presentation.api.subsonic.response_builder import (
    build_error_response,
    build_response,
)
from presentation.api.subsonic.routers.dependencies import (
    SubsonicAuthContext,
    subsonic_auth,
)

system_router = APIRouter()


def _auth_error(auth: SubsonicAuthContext, response_format: str) -> Response:
    return build_error_response(auth.error_code or 40, response_format, auth.error_message)


@system_router.get("/ping")
@system_router.get("/ping.view")
async def ping(
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("xml")
) -> Response:
    if auth.is_authenticated:
        return build_response({}, f)
    return _auth_error(auth, f)


@system_router.get("/getLicense")
@system_router.get("/getLicense.view")
async def get_license(
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("xml")
) -> Response:
    if auth.is_authenticated:
        data = {"license": {"valid": True}}
        return build_response(data, f)
    return _auth_error(auth, f)
