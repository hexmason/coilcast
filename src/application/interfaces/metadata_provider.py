from abc import abstractmethod
from pathlib import Path
from typing import Any, Dict, Protocol


class MetadataProvider(Protocol):
    @staticmethod
    @abstractmethod
    def get_track_metadata(track_path: Path) -> Dict[str, Any]: ...
