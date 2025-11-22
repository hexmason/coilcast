from dataclasses import dataclass


@dataclass(frozen=True)
class MediaFileMetadata:
    path: str
    size: int
    mtime: float
    hash: str
    suffix: str
    # offset: float
    # subtrack: int
    bit_rate: int
    bit_depth: int
    sampling_rate: int
    channel_count: int
