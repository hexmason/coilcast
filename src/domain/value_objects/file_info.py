from dataclasses import dataclass


@dataclass(frozen=True)
class FileInfo:
    path: str
    size: int
    mtime: float
    hash: str
    suffix: str
