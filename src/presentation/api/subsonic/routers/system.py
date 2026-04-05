 from fastapi import APIRouter, Response
# from presentation.schemas.responses import SubsonicResponseFactory
 from presentation.api.routers.subsonic.dependencies import ParametersDep

 router = APIRouter()

 @router.get("/ping")
 async def ping(params: ParametersDep) -> Response:
    return SubsonicResponseFactory(response_format=params.f).get_response()


 @router.get("/getLicense")
 async def get_license(params: ParametersDep) -> Response:
    return SubsonicResponseFactory(response_format=params.f).get_response()


