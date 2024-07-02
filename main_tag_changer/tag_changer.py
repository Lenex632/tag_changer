import re
import eyed3
import logging

from eyed3.core import AudioFile
from pathlib import Path

from model import Track
from logger import set_up_logger_config


class TagChanger:
    def __init__(self, target_dir: str, artist_dirs: list[str]) -> None:
        set_up_logger_config()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.target_dir = Path(target_dir)
        self.artist_dirs = artist_dirs

        # цыфры + скобки|пробелы|точки|прочее
        self.pattern_to_number = re.compile(r'^\d+(\W | \W | |\)|\) )')
        self.pattern_to_feat = re.compile(r'(\(|\s)(feat|Feat|ft|Ft)(\. |\.| )(?P<other>.*?)(\)|$)')

    def find_numbers(self, target: str) -> str:
        target = self.pattern_to_number.sub('', target)
        self.logger.debug(f'"{target}"')

        return target

    @staticmethod
    def split_artist(target: str) -> [str, list[str]]:
        target = target.split(',')
        target = [s.strip() for s in target]
        artist = target.pop(0)

        return artist, target

    def find_feats(self, target: str) -> [str, list[str]]:
        feats = []
        match = self.pattern_to_feat.search(target)

        if match:
            target = self.pattern_to_feat.sub('', target)
            match = self.pattern_to_feat.search(match.group())
            feats = match.group('other').split(',')

        return target, feats


if __name__ == '__main__':
    a = TagChanger('a', ['a', 'b'])
    print(a.find_feats('name'))
    print(a.find_feats('name (feat. other2)'))
    print(a.find_feats('name (feat. other1, other2)'))
    print(a.find_feats('name feat. other1, other2'))
