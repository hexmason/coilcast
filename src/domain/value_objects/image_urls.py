from dataclasses import dataclass


@dataclass(frozen=True)
class ImageUrls:
    small: str
    medium: str
    large: str
