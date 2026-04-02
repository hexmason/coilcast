from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TrackMetadataDTO:
    title: str | None
    album: str | None
    artist: str | None
    album_artist: str | None
    track_number: int | None
    disc_number: int | None
    year: int | None
    duration: float | None
    compilation: bool | None
    genre: List[str] | None
    bit_rate: int | None
    bit_depth: int | None
    sampling_rate: int | None
    channel_count: int | None
