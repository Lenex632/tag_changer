from dataclasses import dataclass
from pathlib import Path


@dataclass
class SongData:
    file_path: Path
    title: str
    artist: str
    album: str
    feat: str | None = None
    special: str | None = None
    image: Path | None = None


@dataclass
class TableModel:
    song_id: str = 'INTEGER PRIMARY KEY AUTOINCREMENT'
    file_path: str = 'TEXT'
    title: str = 'TEXT'
    artist: str = 'TEXT'
    album: str = 'TEXT'
    feat: str = 'TEXT'
    special: str = 'TEXT'
    image: str = 'TEXT'
