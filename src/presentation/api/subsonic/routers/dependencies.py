from dataclasses import dataclass
from hashlib import md5

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from application.config.settings import settings
from application.use_cases.album import GetAlbumWithSongsUseCase
from application.use_cases.artist import GetArtistWithAlbumsUseCase, GetArtistsUseCase
from application.use_cases.media_file import GetMediaFileUseCase
from infrastructure.database.unit_of_work import UnitOfWork
from infrastructure.database.utils import get_session


@dataclass
class SubsonicAuthContext:
    user: dict | None
    error_code: int | None = None
    error_message: str | None = None

    @property
    def is_authenticated(self) -> bool:
        return self.user is not None


def _is_valid_token(password: str, token: str, salt: str) -> bool:
    expected = md5((password + salt).encode("utf-8")).hexdigest()
    return token == expected


def _decode_legacy_password(password: str) -> str:
    if not password.startswith("enc:"):
        return password
    try:
        return bytes.fromhex(password[4:]).decode("utf-8")
    except ValueError:
        return ""


def subsonic_auth(
    u: str | None = Query(None),
    p: str | None = Query(None),
    t: str | None = Query(None),
    s: str | None = Query(None),
    v: str | None = Query(None),
    c: str | None = Query(None),
) -> SubsonicAuthContext:
    if not u or not v or not c:
        return SubsonicAuthContext(None, 10, "Required parameter is missing")

    if u != settings.ADMIN_LOGIN:
        return SubsonicAuthContext(None, 40, "Wrong username or password")

    if p and (t or s):
        return SubsonicAuthContext(
            None, 43, "Multiple conflicting authentication mechanisms provided"
        )

    if p:
        decoded = _decode_legacy_password(p)
        if decoded != settings.ADMIN_PASS:
            return SubsonicAuthContext(None, 40, "Wrong username or password")
    elif t and s:
        if not _is_valid_token(settings.ADMIN_PASS, t, s):
            return SubsonicAuthContext(None, 40, "Wrong username or password")
    else:
        return SubsonicAuthContext(None, 10, "Missing credentials")

    return SubsonicAuthContext(
        {
            "id": "admin",
            "username": settings.ADMIN_LOGIN,
            "is_admin": True,
        }
    )


def get_uow(session: AsyncSession = Depends(get_session)) -> UnitOfWork:
    return UnitOfWork(session)


def get_artist_use_case(
    uow: UnitOfWork = Depends(get_uow),
) -> GetArtistWithAlbumsUseCase:
    return GetArtistWithAlbumsUseCase(uow)


def get_artists_use_case(
    uow: UnitOfWork = Depends(get_uow),
) -> GetArtistsUseCase:
    return GetArtistsUseCase(uow)


def get_album_use_case(
    uow: UnitOfWork = Depends(get_uow),
) -> GetAlbumWithSongsUseCase:
    return GetAlbumWithSongsUseCase(uow)


def get_media_file_use_case(
    uow: UnitOfWork = Depends(get_uow),
) -> GetMediaFileUseCase:
    return GetMediaFileUseCase(uow)
