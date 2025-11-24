from dataclasses import dataclass, field


@dataclass(frozen=True)
class ImageUrls:
    small: str = field(default="")
    medium: str = field(default="")
    large: str = field(default="")
