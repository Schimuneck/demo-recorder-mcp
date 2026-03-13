"""
Core module - shared types and configuration.
"""

from .config import (
    VIDEO_SERVER_HOST,
    VIDEO_SERVER_PORT,
    get_ffmpeg_path,
    get_media_url,
    get_recordings_dir,
    is_container_environment,
)
from .types import (
    RecordingResult,
    RecordingState,
    WindowBounds,
    WindowInfo,
)

__all__ = [
    # Types
    "WindowBounds",
    "WindowInfo",
    "RecordingResult",
    "RecordingState",
    # Config
    "get_recordings_dir",
    "get_ffmpeg_path",
    "is_container_environment",
    "get_media_url",
    "VIDEO_SERVER_PORT",
    "VIDEO_SERVER_HOST",
]
