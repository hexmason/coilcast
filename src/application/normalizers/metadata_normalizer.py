from re import search
from dateutil.parser import parse
from typing import Any, Dict, Optional


class MetadataNormalizer:
    @staticmethod
    def _first(value: Any) -> Optional[Any]:
        if isinstance(value, list):
            return value[0] if value else None
        return value

    @staticmethod
    def _extract_track_number(value: Any) -> Optional[int]:
        value = MetadataNormalizer._first(value)

        if not value:
            return None

        if "/" in value:
            num, _ = value.split("/", 1)
            return int(num) if num.isdigit() else None

        return int(value) if value.isdigit() else None

    @staticmethod
    def _extract_year(date: Any) -> Optional[int]:
        if not date:
            return None

        try:
            dt = parse(date, fuzzy=True, default=None)
            return dt.year
        except Exception:
            match = search(r"\b(\d{4})\b", date)
            if match:
                return int(match.group(1))
            return None

    @staticmethod
    def normalize(raw: Dict[str, Any]) -> Dict[str, Any]:
        normalized = {}

        normalized["title"] = MetadataNormalizer._first(raw.get("title"))
        normalized["artist"] = MetadataNormalizer._first(raw.get("artist"))
        normalized["album"] = MetadataNormalizer._first(raw.get("album"))
        normalized["album_artist"] = MetadataNormalizer._first(raw.get("albumartist"))
        normalized["genre"] = MetadataNormalizer._first(raw.get("genre"))
        normalized["year"] = MetadataNormalizer._extract_year(
            MetadataNormalizer._first(raw.get("date"))
        )

        track = MetadataNormalizer._extract_track_number(raw.get("tracknumber"))
        normalized["track_number"] = track

        disc = MetadataNormalizer._extract_track_number(raw.get("discnumber"))
        normalized["disc_number"] = disc

        normalized["bit_rate"] = raw.get("bitrate")
        normalized["bit_depth"] = raw.get("bits_per_sample")
        normalized["sampling_rate"] = raw.get("sample_rate")
        normalized["channel_count"] = raw.get("channels")
        normalized["duration"] = raw.get("length")

        return normalized
