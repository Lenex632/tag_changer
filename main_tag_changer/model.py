from dataclasses import dataclass
from pathlib import Path


@dataclass
class SongData:
    file_path: str | Path
    title: str
    artist: str
    album: str
    feat: list
    special: str
    image: Path | None = None
    timestamp: str = None
