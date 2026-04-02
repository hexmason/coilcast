from infrastructure.providers.dto import TrackMetadataDTO


def track_metadata_to_dto(data: dict) -> TrackMetadataDTO:
    return TrackMetadataDTO(
        title=data.get("title"),
        album=data.get("album"),
        artist=data.get("artist"),
        album_artist=data.get("album_artist", data.get("albumartist")),
        track_number=data.get("track_number", data.get("tracknumber")),
        disc_number=data.get("disc_number", data.get("discnumber")),
        year=data.get("year"),
        duration=data.get("duration", data.get("length")),
        compilation=data.get("compilation"),
        genre=data.get("genre"),
        bit_rate=data.get("bit_rate", data.get("bitrate")),
        bit_depth=data.get("bit_depth"),
        sampling_rate=data.get("sampling_rate", data.get("sample_rate")),
        channel_count=data.get("channel_count", data.get("channels")),
    )
