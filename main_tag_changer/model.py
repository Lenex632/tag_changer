from dataclasses import dataclass
from pathlib import Path


@dataclass
class SongData:
    file_path: str | Path = None
    title: str = None
    artist: str = None
    album: str = None
    feat: bool | str = None
    special: bool | str = None
    image: bool | Path = None
    timestamp: str = None
