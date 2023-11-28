from dataclasses import dataclass
from pathlib import Path


@dataclass
class MusicData:
    library: str = None
    file_path: str | Path = None
    title: str = None
    artist: str = None
    album: str = None
    image: bool | Path = None
