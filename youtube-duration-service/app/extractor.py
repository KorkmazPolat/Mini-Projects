import re
from typing import Dict, Optional
from urllib.parse import urlparse, parse_qs


class ExtractionError(Exception):
    pass


def seconds_to_hms(total_seconds: int) -> str:
    if total_seconds is None:
        return "00:00:00"
    total_seconds = int(total_seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def parse_iso8601_duration(duration: str) -> int:
    # Retained for potential future use; not used without API
    pattern = re.compile(r"^PT(?:(?P<h>\d+)H)?(?:(?P<m>\d+)M)?(?:(?P<s>\d+)S)?$")
    match = pattern.match(duration)
    if not match:
        raise ExtractionError(f"Unrecognized ISO8601 duration: {duration}")
    hours = int(match.group('h') or 0)
    minutes = int(match.group('m') or 0)
    seconds = int(match.group('s') or 0)
    return hours * 3600 + minutes * 60 + seconds


def extract_youtube_id(url: str) -> Optional[str]:
    try:
        parsed = urlparse(url)
    except Exception:
        return None

    # Query param 'v'
    qs = parse_qs(parsed.query)
    if 'v' in qs and qs['v']:
        return qs['v'][0]

    # Path-based formats
    path = parsed.path.strip('/')
    parts = path.split('/') if path else []
    if not parts:
        return None

    # youtu.be/<id>
    if parsed.netloc in {"youtu.be"}:
        return parts[0] if parts[0] else None

    # youtube.com/shorts/<id>
    if len(parts) >= 2 and parts[0] in {"shorts", "embed", "v", "live"}:
        return parts[1]

    # As a last resort, try to find 11-char video IDs in path
    m = re.search(r"([A-Za-z0-9_-]{11})", path)
    if m:
        return m.group(1)

    return None


def _extract_with_ytdlp(url: str) -> Dict:
    try:
        # Import locally to keep it optional
        from yt_dlp import YoutubeDL  # type: ignore
    except Exception as e:
        raise ExtractionError(f"yt-dlp not available: {e}")

    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'skip_download': True,
        'nocheckcertificate': True,
        'socket_timeout': 10,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        raise ExtractionError(f"yt-dlp failed: {e}")

    duration = info.get('duration')
    title = info.get('title')
    vid = info.get('id')
    if duration is None or vid is None:
        raise ExtractionError("Missing duration or id in yt-dlp info")

    return {
        'id': vid,
        'title': title or '',
        'duration_seconds': int(duration),
        'duration_human': seconds_to_hms(int(duration)),
        'source': 'yt_dlp',
    }


def get_duration_info(url: str) -> Dict:
    # Use yt-dlp only (no API key)
    try:
        return _extract_with_ytdlp(url)
    except ExtractionError as e:
        raise ExtractionError(
            "Failed to extract duration with yt-dlp. Ensure 'yt-dlp' is installed and the URL is valid."
        ) from e
