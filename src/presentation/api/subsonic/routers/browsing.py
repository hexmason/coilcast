from fastapi import APIRouter, Response, Query, Depends
from presentation.api.subsonic.response_builder import (
    build_error_response,
    build_response,
)
from presentation.api.subsonic.routers.dependencies import (
    SubsonicAuthContext,
    subsonic_auth,
)
from application.use_cases.artist import GetArtistWithAlbumsUseCase, GetArtistsUseCase
from application.use_cases.album import GetAlbumWithSongsUseCase
from presentation.api.subsonic.mappers.artist import to_get_artist_response
from presentation.api.subsonic.mappers.album import to_get_album_response

browsing_router = APIRouter()


@browsing_router.get("/getMusicFolders")
async def get_music_folders(
    auth: SubsonicAuthContext = Depends(subsonic_auth), f: str = Query("json")
) -> Response:
    data = {"musicFolders": {"musicFolder": [{"id": 1, "name": "music"}]}}
    return build_response(data, f)


@browsing_router.get("/getArtists")
async def get_artists(
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("json"),
    use_case: GetArtistsUseCase = Depends(),
) -> Response:

    artists = use_case.execute(auth.user.id)

    data = {"artists": {"index": build_indexed_artists(artists)}}

    return build_response(data, f)


@browsing_router.get("/getArtist")
async def get_artist(
    id: int = Query(...),
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("json"),
    use_case: GetArtistWithAlbumsUseCase = Depends(),
) -> Response:

    artist = use_case.execute(id)

    data = to_get_artist_response(artist)

    return build_response(data, f)


@browsing_router.get("/getAlbum")
async def get_album(
    id: int = Query(...),
    auth: SubsonicAuthContext = Depends(subsonic_auth),
    f: str = Query("json"),
    use_case: GetAlbumWithSongsUseCase = Depends(),
) -> Response:

    album = use_case.execute(id)

    data = to_get_album_response(album)

    return build_response(data, f)
