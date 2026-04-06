from time import time
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response

from application.config.settings import settings
from application.use_cases.album import GetAlbumWithSongsUseCase
from application.use_cases.artist import GetArtistWithAlbumsUseCase, GetArtistsUseCase
from application.use_cases.media_file import GetMediaFileUseCase
from presentation.api.subsonic.mappers.album import to_album_entry, to_get_album_response
from presentation.api.subsonic.mappers.artist import (
    to_get_artist_response,
    to_indexes_response,
)
from presentation.api.subsonic.mappers.media_file import to_get_song_response, to_song_entry
from presentation.api.subsonic.response_builder import build_error_response, build_response
from presentation.api.subsonic.routers.dependencies import (
    SubsonicAuthContext,
    get_album_use_case,
    get_artist_use_case,
    get_artists_use_case,
    get_media_file_use_case,
    subsonic_auth,
)

browsing_router = APIRouter()


def _auth_error(auth: SubsonicAuthContext, response_format: str) -> Response:
    return build_error_response(auth.error_code or 40, response_format, auth.error_message)


def _parse_uuid(raw_id: str) -> UUID | None:
    try:
        return UUID(raw_id)
    except ValueError:
        return None


@browsing_router.get("/getMusicFolders")
@browsing_router.get("/getMusicFolders.view")
async def get_music_folders(
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("xml"),
) -> Response:
    if not auth.is_authenticated:
        return _auth_error(auth, f)

    data = {
        "musicFolders": {
            "musicFolder": [
                {"@id": 1, "@name": settings.MUSIC_FOLDER.name or "music"}
            ]
        }
    }
    return build_response(data, f)


@browsing_router.get("/getArtists")
@browsing_router.get("/getArtists.view")
async def get_artists(
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("xml"),
    use_case: GetArtistsUseCase = Depends(get_artists_use_case),
) -> Response:
    if not auth.is_authenticated:
        return _auth_error(auth, f)

    artists = await use_case.execute()
    data = {"artists": to_indexes_response(artists)}
    return build_response(data, f)


@browsing_router.get("/getIndexes")
@browsing_router.get("/getIndexes.view")
async def get_indexes(
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("xml"),
    use_case: GetArtistsUseCase = Depends(get_artists_use_case),
) -> Response:
    if not auth.is_authenticated:
        return _auth_error(auth, f)

    artists = await use_case.execute()
    indexes = to_indexes_response(artists)
    data = {
        "indexes": {
            "@lastModified": int(time() * 1000),
            "@ignoredArticles": "The El La Los Las Le Les",
            **indexes,
        }
    }
    return build_response(data, f)


@browsing_router.get("/getArtist")
@browsing_router.get("/getArtist.view")
async def get_artist(
    id: str = Query(...),
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("xml"),
    use_case: GetArtistWithAlbumsUseCase = Depends(get_artist_use_case),
) -> Response:
    if not auth.is_authenticated:
        return _auth_error(auth, f)

    artist_id = _parse_uuid(id)
    if artist_id is None:
        return build_error_response(10, f)

    artist = await use_case.execute(artist_id)
    if artist is None:
        return build_error_response(70, f)

    return build_response(to_get_artist_response(artist), f)


@browsing_router.get("/getAlbum")
@browsing_router.get("/getAlbum.view")
async def get_album(
    id: str = Query(...),
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("xml"),
    use_case: GetAlbumWithSongsUseCase = Depends(get_album_use_case),
) -> Response:
    if not auth.is_authenticated:
        return _auth_error(auth, f)

    album_id = _parse_uuid(id)
    if album_id is None:
        return build_error_response(10, f)

    album = await use_case.execute(album_id)
    if album is None:
        return build_error_response(70, f)

    return build_response(to_get_album_response(album), f)


@browsing_router.get("/getSong")
@browsing_router.get("/getSong.view")
async def get_song(
    id: str = Query(...),
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("xml"),
    use_case: GetMediaFileUseCase = Depends(get_media_file_use_case),
) -> Response:
    if not auth.is_authenticated:
        return _auth_error(auth, f)

    song_id = _parse_uuid(id)
    if song_id is None:
        return build_error_response(10, f)

    song = await use_case.execute(song_id)
    if song is None:
        return build_error_response(70, f)

    return build_response(to_get_song_response(song), f)


@browsing_router.get("/getMusicDirectory")
@browsing_router.get("/getMusicDirectory.view")
async def get_music_directory(
    id: str = Query(...),
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("xml"),
    artist_use_case: GetArtistWithAlbumsUseCase = Depends(get_artist_use_case),
    album_use_case: GetAlbumWithSongsUseCase = Depends(get_album_use_case),
) -> Response:
    if not auth.is_authenticated:
        return _auth_error(auth, f)

    object_id = _parse_uuid(id)
    if object_id is None:
        return build_error_response(10, f)

    artist = await artist_use_case.execute(object_id)
    if artist is not None:
        data = {
            "directory": {
                "@id": str(artist.id),
                "@name": artist.name,
                "child": [to_album_entry(album) for album in artist.albums],
            }
        }
        return build_response(data, f)

    album = await album_use_case.execute(object_id)
    if album is not None:
        data = {
            "directory": {
                "@id": str(album.id),
                "@name": album.name,
                "child": [to_song_entry(song) for song in album.media_files],
            }
        }
        return build_response(data, f)

    return build_error_response(70, f)
