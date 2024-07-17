import re
import eyed3
import logging

from eyed3.core import AudioFile
from pathlib import Path

from model import SongData


# TODO
#  Сначала избавляемся от номера (check)
#  Потом разделяем Title и Artist (check)
#  Обработали Title и Artist на feat (check)
#  Обработали Title на OP EN скобки (check)
#  Обработали Title, Album на мусорные скобки (check)
#  Разделили на Artist и Other (check)
#  Объединили Title + feat. + OP EN (check)
class TagChanger:
    def __init__(self, target_dir: str, artist_dirs: list[str]) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.target_dir = Path(target_dir)
        self.artist_dirs = map(Path, artist_dirs)

        # цифры + скобки|пробелы|точки|прочее
        self.pattern_to_number = re.compile(r'^\d+(\W | \W | |\)|\) )')
        # feat
        self.pattern_to_feat = re.compile(r'(\(|\s)(feat|Feat|ft|Ft)(\. |\.| )(?P<feats>.*?)(\)|$)')
        # опенинги/эндинги TODO в будущем мб можно сделать под кастомные запросы
        self.pattern_to_special = re.compile(r'\((OP|EN)(\d? |\d).*?\)')
        # мусорные скобки
        self.pattern_to_brackets = re.compile(r'([(\[].*?[)\]])(?![\s$]?\w)')

    def delete_numbers(self, target: str) -> str:
        target = self.pattern_to_number.sub('', target)
        self.logger.debug(f'delete_numbers result: {target=}')

        return target

    def split_fullname(self, target: str) -> [str, str]:
        try:
            artist, title = target.split(' - ')
        except ValueError:
            artist = ''
            title = target

        self.logger.debug(f'split_fullname result: {artist=}, {title=}')

        return artist, title

    def split_artist(self, target: str) -> [str, list[str]]:
        target = target.split(',')
        feat = [s.strip() for s in target]
        artist = feat.pop(0)
        self.logger.debug(f'split_artist result: {artist=}, {feat=}')

        return artist, feat

    def find_feats(self, target: str) -> [str, list[str]]:
        feat = []
        match = self.pattern_to_feat.search(target)

        if match:
            self.logger.debug(f'{match.group()}, {match.group("feats")=}')
            target = target.replace(match.group(), '').strip()
            feat = match.group('feats').split(',')
            feat = [feat.strip() for feat in feat]

        self.logger.debug(f'find_feats result: {target=}, {feat=}')

        return target, feat

    def find_special(self, target: str) -> [str, str]:
        special = ''
        match = self.pattern_to_special.search(target)

        if match:
            special = match.group()
            target = target.replace(special, '').strip()

        self.logger.debug(f'find_special result: {target=}, {special=}')

        return target, special

    def delete_brackets(self, target: str) -> str:
        target = self.pattern_to_brackets.sub('', target).strip()
        self.logger.debug(f'delete_brackets result: {target=}')

        return target

    def merge(self, title: str, feat: list, special: str) -> str:
        target = title
        if feat:
            target += f' (feat. {", ".join(feat)})'
        if special:
            target += f' {special}'
        self.logger.debug(f'merge result: {target=}')

        return target

    def get_info_from_file(self, file: Path) -> [str, str, str, str]:
        self.logger.debug(f'{file.stem}')
        target = self.delete_numbers(file.stem)
        artist, title = self.split_fullname(target)
        artist, feat1 = self.split_artist(artist)
        artist, feat2 = self.find_feats(artist)
        title, feat3 = self.find_feats(title)
        feat = feat1 + feat2 + feat3
        title, special = self.find_special(title)
        title = self.delete_brackets(title)

        return artist, title, feat, special

    def start(self, directory: Path):
        for file_path in directory.iterdir():
            file = file_path.relative_to(self.target_dir)
            level = len(file.parts) - 1

            if file_path.is_dir():
                self.logger.debug(f'{"---" * level}|{file.name}')
                self.start(file_path)
            elif file_path.is_file() and file.suffix != '.jpg':
                self.logger.debug(f'{"---" * level}>{file.name}')
                artist, title, feat, special = self.get_info_from_file(file_path)


if __name__ == '__main__':
    from logger import set_up_logger_config
    set_up_logger_config()

    a = TagChanger('C:\\code\\tag_changer\\test_tag_change', ['a', 'b'])
    a.start(a.target_dir)
