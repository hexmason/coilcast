def get_content_type(suffix: str) -> str:
    suffix = suffix.lower().lstrip(".")

    audio_types = {
        "mp3": "audio/mpeg",
        "flac": "audio/flac",
        "wav": "audio/wav",
        "ogg": "audio/ogg",
        "aac": "audio/aac",
        "m4a": "audio/mp4",
        "wma": "audio/x-ms-wma",
        "alac": "audio/alac",
        "aiff": "audio/aiff",
    }

    return audio_types.get(suffix, "application/octet-stream")
