from pathlib import Path

from infrastructure.providers.dto.file_info import FileInfoDTO


class FileInfoProvider:
    @staticmethod
    def get_file_info(file_path: Path) -> FileInfoDTO:
        stat = file_path.stat()
        return FileInfoDTO(
                path=file_path,
                size=stat.st_size,
                mtime=stat.st_mtime,
                suffix=file_path.suffix.lower()
            )
