import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query, Response

from application.config.settings import settings
from application.services.library_scanner import LibraryScannerService
from application.services.library_sync import LibrarySyncService
from infrastructure.database.engine import AsyncSessionLocal
from infrastructure.database.unit_of_work import UnitOfWork
from infrastructure.providers.mutagen_metadata import MutagenMetadataProvider
from presentation.api.subsonic.response_builder import build_error_response, build_response
from presentation.api.subsonic.routers.dependencies import SubsonicAuthContext, subsonic_auth

media_library_scanning_router = APIRouter()

_scan_status = {
    "scanning": False,
    "count": 0,
    "started_at": None,
    "finished_at": None,
    "error": None,
}
_scan_lock = asyncio.Lock()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _auth_error(auth: SubsonicAuthContext, response_format: str) -> Response:
    return build_error_response(auth.error_code or 40, response_format, auth.error_message)


def _scan_status_payload() -> dict:
    payload = {
        "@scanning": _scan_status["scanning"],
        "@count": _scan_status["count"],
    }
    if _scan_status["started_at"]:
        payload["@startedAt"] = _scan_status["started_at"]
    if _scan_status["finished_at"]:
        payload["@finishedAt"] = _scan_status["finished_at"]
    if _scan_status["error"]:
        payload["@error"] = _scan_status["error"]
    return payload


async def _run_scan() -> None:
    async with _scan_lock:
        _scan_status["scanning"] = True
        _scan_status["error"] = None
        _scan_status["count"] = 0
        _scan_status["started_at"] = _utc_now_iso()
        _scan_status["finished_at"] = None

        try:
            async with AsyncSessionLocal() as session:
                uow = UnitOfWork(session)
                scanner_service = LibraryScannerService(settings.MUSIC_FOLDER)
                metadata_provider = MutagenMetadataProvider()
                sync_service = LibrarySyncService(scanner_service, metadata_provider, uow)
                seen_paths = await sync_service.sync()
                _scan_status["count"] = len(seen_paths)
        except Exception as exc:
            _scan_status["error"] = str(exc)
        finally:
            _scan_status["scanning"] = False
            _scan_status["finished_at"] = _utc_now_iso()


@media_library_scanning_router.get("/startScan")
@media_library_scanning_router.get("/startScan.view")
async def start_scan(
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("xml"),
) -> Response:
    if not auth.is_authenticated:
        return _auth_error(auth, f)

    if not _scan_status["scanning"]:
        asyncio.create_task(_run_scan())

    return build_response({"scanStatus": _scan_status_payload()}, f)


@media_library_scanning_router.get("/getScanStatus")
@media_library_scanning_router.get("/getScanStatus.view")
async def get_scan_status(
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("xml"),
) -> Response:
    if not auth.is_authenticated:
        return _auth_error(auth, f)

    return build_response({"scanStatus": _scan_status_payload()}, f)
