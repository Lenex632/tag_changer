import re
import eyed3
import logging

from eyed3.core import AudioFile
from pathlib import Path

from model import Track
from logger import set_up_logger_config


# TODO
#  Сначала избавляемся от номера (check)
#  Потом разделяем Title и Artist (check)
#  Обработали Title и Artist на feat (check)
#  Обработали Title на OP EN скобки
#  Обработали Title, Album на мусорные скобки
#  Разделили на Artist и Other (check)
#  Объединили Title + feat. + OP EN
class TagChanger:
    def __init__(self, target_dir: str, artist_dirs: list[str]) -> None:
        set_up_logger_config()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.target_dir = Path(target_dir)
        self.artist_dirs = artist_dirs

        # цифры + скобки|пробелы|точки|прочее
        self.pattern_to_number = re.compile(r'^\d+(\W | \W | |\)|\) )')
        self.pattern_to_feat = re.compile(r'(\(|\s)(feat|Feat|ft|Ft)(\. |\.| )(?P<feats>.*?)(\)|$)')
        self.pattern_to_anime = re.compile(r'\((OP|EN)(\d? |\d).*?\)')

    def find_numbers(self, target: str) -> str:
        target = self.pattern_to_number.sub('', target)
        self.logger.debug(f'{target=}')

        return target

    def split_fullname(self, target: str) -> [str, str]:
        try:
            artist, title = target.split(' - ')
        except ValueError:
            artist = ''
            title = target

        self.logger.debug(f'{artist=}, {title=}')

        return artist, title

    def find_feats(self, target: str) -> [str, list[str]]:
        feats = []
        match = self.pattern_to_feat.search(target)

        if match:
            self.logger.debug(f'{match.group()}, {match.group("feats")=}')
            target = target.replace(match.group(), '').strip()
            feats = match.group('feats').split(',')
            feats = [feat.strip() for feat in feats]

        self.logger.debug(f'{target=}, {feats=}')

        return target, feats

    def find_anime(self, target: str) -> [str, str]:
        anime = ''
        match = self.pattern_to_anime.search(target)

        if match:
            anime = match.group()
            target = target.replace(anime, '').strip()

        self.logger.debug(f'{target=}, {anime=}')

        return target, anime

    def split_artist(self, target: str) -> [str, list[str]]:
        target = target.split(',')
        other = [s.strip() for s in target]
        artist = other.pop(0)
        self.logger.debug(f'{artist=}, {other=}')

        return artist, other


if __name__ == '__main__':
    a = TagChanger('a', ['a', 'b'])
