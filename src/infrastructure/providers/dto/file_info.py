from blake3 import blake3
from pathlib import Path
from dataclasses import dataclass
from functools import cached_property


@dataclass(frozen=True)
class FileInfoDTO:
    path: Path
    size: int
    mtime: float
    suffix: str

    @cached_property
    def hash(self) -> str:
        return blake3(self.path.read_bytes()).hexdigest()
