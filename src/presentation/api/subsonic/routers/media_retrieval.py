from fastapi import APIRouter, Response, Query, Depends
from fastapi.responses import StreamingResponse
from application.use_cases.media_file import GetMediaFileUseCase
from presentation.api.subsonic.response_builder import (
    build_error_response,
    build_response,
)
from presentation.api.subsonic.routers.dependencies import (
    SubsonicAuthContext,
    subsonic_auth,
)

media_retrieval_router = APIRouter()


@media_retrieval_router.get("/stream")
async def stream(
    id: int = Query(...),
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    use_case: GetMediaFileUseCase = Depends(),
) -> Response:

    file_path = use_case.execute(id)
    file = open(file_path, "rb")

    return StreamingResponse(file, media_type="audio/mpeg")
