from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import FileResponse

from application.config.settings import settings
from application.use_cases.media_file import GetMediaFileUseCase
from presentation.api.subsonic.response_builder import build_error_response
from presentation.api.subsonic.routers.dependencies import (
    SubsonicAuthContext,
    get_media_file_use_case,
    subsonic_auth,
)
from presentation.api.subsonic.utils import get_content_type

media_retrieval_router = APIRouter()


def _auth_error(auth: SubsonicAuthContext, response_format: str) -> Response:
    return build_error_response(auth.error_code or 40, response_format, auth.error_message)


def _resolve_media_path(path: str) -> Path:
    source = Path(path)
    candidates = [source, Path.cwd() / source]
    project_root = Path(__file__).resolve().parents[5]
    candidates.append(project_root / source)
    if not source.is_absolute():
        candidates.append(project_root / settings.MUSIC_FOLDER / source)

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return source


@media_retrieval_router.get("/stream")
@media_retrieval_router.get("/stream.view")
async def stream(
    id: str = Query(...),
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("xml"),
    use_case: GetMediaFileUseCase = Depends(get_media_file_use_case),
) -> Response:
    if not auth.is_authenticated:
        return _auth_error(auth, f)

    try:
        media_id = UUID(id)
    except ValueError:
        return build_error_response(10, f)

    media_file = await use_case.execute(media_id)
    if media_file is None:
        return build_error_response(70, f)

    file_path = _resolve_media_path(media_file.file_info.path)
    if not file_path.exists():
        return build_error_response(70, f, "Audio file does not exist on disk")

    return FileResponse(
        path=file_path,
        media_type=get_content_type(media_file.file_info.suffix),
        filename=file_path.name,
    )
