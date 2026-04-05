from pathlib import Path
from typing import AsyncIterator

from application.config.constants import MEDIA_FILE_EXTENSIONS
from infrastructure.providers import FileInfoProvider
from infrastructure.providers.dto.file_info import FileInfoDTO


class LibraryScannerService:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path

    async def scan(self) -> AsyncIterator[FileInfoDTO]:
        for path in Path(self.root_path).rglob("*"):
            if path.suffix.lower() in MEDIA_FILE_EXTENSIONS:
                yield FileInfoProvider.get_file_info(path)
