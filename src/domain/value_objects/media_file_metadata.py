from dataclasses import dataclass, field


@dataclass(frozen=True)
class MediaFileMetadata:
    # offset: float
    # subtrack: int
    bit_rate: int = field(default=0)
    bit_depth: int = field(default=0)
    sampling_rate: int = field(default=0)
    channel_count: int = field(default=0)
