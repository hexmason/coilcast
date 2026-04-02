import os
from mutagen import File
from pathlib import Path
from typing import Any, Dict

from application.interfaces.metadata_provider import MetadataProvider


class MutagenMetadataProvider(MetadataProvider):
    @staticmethod
    def get_track_metadata(track_path: Path) -> Dict[str, Any]:
        if not os.path.isfile(track_path):
            raise FileNotFoundError(f"File not found: {track_path}.")

        audio = File(track_path, easy=True)
        audio_raw = File(track_path)

        if audio is None:
            raise ValueError(
                f"Unsupported or unrecognized file format: {track_path}."
            )

        metadata = {}
        tech_tags = [
            "bitrate",
            "bits_per_sample",
            "sample_rate",
            "channels",
            "length"
        ]

        for key in audio.keys():
            metadata[f"{key}"] = audio.tags.get(f"{key}")

        for key in tech_tags:
            metadata[f"{key}"] = getattr(audio_raw.info, f"{key}", None)

        return metadata
