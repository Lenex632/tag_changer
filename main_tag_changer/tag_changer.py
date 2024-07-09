import re
import eyed3
import logging

from eyed3.core import AudioFile
from pathlib import Path

from model import Track
from logger import set_up_logger_config


# TODO
#  Сначала избавляемся от номера
#  Потом разделяем Title и Artist
#  Обработали Title и Artist на feat
#  Обработали Title на OP EN скобки
#  Обработали Title, Album на мусорные скобки
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
        other = [s.strip() for s in target]
        artist = other.pop(0)

        return artist, other

    def find_feats(self, target: str) -> [str, list[str]]:
        artist = target
        feats = []
        match = self.pattern_to_feat.search(target)

        if match:
            artist = self.pattern_to_feat.sub('', target).strip()
            match = self.pattern_to_feat.search(match.group())
            feats = match.group('other').split(',')
            feats = [feat.strip() for feat in feats]

        return artist, feats


if __name__ == '__main__':
    a = TagChanger('a', ['a', 'b'])
