import logging
from pathlib import Path
import re

import eyed3

from model import SongData


class TagChanger:
    def __init__(self, target_dir: str, artist_dirs: list[str]) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.target_dir = Path(target_dir)
        self.artist_dirs = artist_dirs

        # цифры + скобки|пробелы|точки|прочее
        self.pattern_to_number = re.compile(r'^\d+(\W | \W | |\)|\) )')
        # feat
        self.pattern_to_feat = re.compile(r'(\(|\s)(feat|Feat|ft|Ft)(\. |\.| )(?P<feats>.*?)(\)|$)')
        # опенинги/эндинги TODO в будущем мб можно сделать под кастомные запросы
        self.pattern_to_special = re.compile(r'\((OP|EN)(\d? |\d).*?\)')
        # мусорные скобки
        self.pattern_to_brackets = re.compile(r'([(\[].*?[)\]])(?![\s$]?\w)')

    def delete_numbers(self, target: str) -> str:
        """Удаление цифр в начале"""
        target = self.pattern_to_number.sub('', target)
        self.logger.debug(f'{target=}')

        return target

    def split_fullname(self, target: str) -> [str, str]:
        """Разделение на artist, title"""
        try:
            artist, title = target.split(' - ')
        except ValueError:
            artist = ''
            title = target

        self.logger.debug(f'{artist=}, {title=}')

        return artist, title

    def split_artist(self, target: str) -> [str, list[str]]:
        """Разделение артистов, что идут через запятую"""
        target = target.split(',')
        feat = [s.strip() for s in target]
        artist = feat.pop(0)
        self.logger.debug(f'{artist=}, {feat=}')

        return artist, feat

    def find_feats(self, target: str) -> [str, list[str]]:
        """Поиск соисполнителей в title и в artist"""
        feat = []
        match = self.pattern_to_feat.search(target)

        if match:
            self.logger.debug(f'{match.group()}, {match.group("feats")=}')
            target = target.replace(match.group(), '').strip()
            feat = match.group('feats').split(',')
            feat = [feat.strip() for feat in feat]

        self.logger.debug(f'{target=}, {feat=}')

        return target, feat

    def find_special(self, target: str) -> [str, str]:
        """Поиск опенингов/эндингов в title"""
        special = ''
        match = self.pattern_to_special.search(target)

        if match:
            special = match.group()
            target = target.replace(special, '').strip()

        self.logger.debug(f'{target=}, {special=}')

        return target, special

    def delete_brackets(self, target: str) -> str:
        """Удаление мусорных скобок"""
        target = self.pattern_to_brackets.sub('', target).strip()
        self.logger.debug(f'{target=}')

        return target

    def merge(self, title: str, feat: list, special: str) -> str:
        """Соединение title, feat и special воедино"""
        target = title
        if feat:
            target += f' (feat. {", ".join(feat)})'
        if special:
            target += f' {special}'
        self.logger.debug(f'{target=}')

        return target

    def get_image(self, file_dir: Path, album: str) -> Path | None:
        """
            Нахождение картинки по пути и названию альбома, если такой нет - создать из первого файла с картинкой, если
            и это нельзя - вернуть None
        """
        self.logger.debug(f'{file_dir}, {album}')
        images = list(file_dir.glob('*.jpg'))
        image_path = Path(file_dir, album + '.jpg')

        if images:
            image = images[0]
            if image.stem != album:
                image.rename(image_path)
            self.logger.debug(f'Get image image {str(image_path)}')
            return image_path
        else:
            for file_path in file_dir.iterdir():
                try:
                    song = eyed3.load(file_path)
                    image = song.tag.images[0].image_data
                    with open(image_path, 'wb+') as album_cover:
                        album_cover.write(image)
                    self.logger.info(f'Create image {str(image_path)}')
                    return image_path
                except IndexError:
                    self.logger.debug(f'AudioFile has no images: {file_path}')
                    continue
                except AttributeError:
                    # TODO узнать при каких условиях может вызваться
                    continue
                except OSError:
                    self.logger.debug(f'eyed3 try to load not an AudioFile: {file_path}')
                    continue

            self.logger.info(f'Cant find image in {file_dir.name} for {album}')
            return None

    def delete_images(self, target_dir: Path) -> None:
        """Удаляет все изображения из target_dir за исключением 'помеченных'"""
        for file in target_dir.iterdir():
            if file.is_dir():
                self.delete_images(file)
            elif file.suffix == '.jpg' and file.parent.name not in ['The Best', 'Nirvana', 'OSU!']:
                self.logger.info(f'Delete image {file}')
                file.unlink()

    def get_info_from_file(self, file_path: Path) -> SongData:
        """
            Достаёт всю информацию из аудиофайла по пути file_path.
            При level=3 изменяет путь до файла.
            Записывает и возвращает все данные в виде SongData
        """
        self.logger.debug(f'{file_path.stem}')

        relative_path = file_path.relative_to(self.target_dir)
        if relative_path.parts[0] in self.artist_dirs:
            level = len(relative_path.parts)
        else:
            level = len(relative_path.parts) - 1

        target = self.delete_numbers(relative_path.stem)
        artist, title = self.split_fullname(target)
        artist, feat1 = self.split_artist(artist)
        artist, feat2 = self.find_feats(artist)
        title, feat3 = self.find_feats(title)
        feat = feat1 + feat2 + feat3
        title, special = self.find_special(title)
        title = self.delete_brackets(title)

        song = eyed3.load(file_path)

        if level == 1:
            # песни в директориях (как в the best)
            album = relative_path.parts[0]
        elif level == 2:
            # песни в директориях и в альбоме
            album = relative_path.parts[1]
        elif level == 3:
            # песни в исполнителе без альбома (создаётся папка с альбомом)
            try:
                album = song.tag.album
            except AttributeError:
                album = 'Without Album'
            album_dir = Path(file_path.parent, album)
            album_dir.mkdir(parents=True, exist_ok=True)
            file_path = file_path.replace(Path(album_dir, file_path.name))
            relative_path = file_path.relative_to(self.target_dir)
        else:
            # песни в исполнителях в альбомах (level == 4)
            artist = relative_path.parts[1]
            album = relative_path.parts[2]
        image = self.get_image(file_path.parent, album)

        return SongData(
            file_path=relative_path,
            title=title,
            artist=artist,
            album=album,
            feat=feat,
            special=special,
            image=image
        )

    def change_tags(self, song_data: SongData) -> None:
        """Сначала стирает все id3 tag из файла, а потом записывает новыми, взятыми из song_data"""
        file_path = Path(self.target_dir, song_data.file_path)
        song = eyed3.load(file_path)
        song.initTag()
        song.tag.remove(file_path)

        title = self.merge(song_data.title, song_data.feat, song_data.special)
        song.tag.title = title
        song.tag.artist = song_data.artist
        song.tag.album = song_data.album
        if song_data.image:
            with open(song_data.image, "rb") as image:
                song.tag.images.set(3, image.read(), "image/jpeg")

        song.tag.save()
        self.logger.info(f'{song_data.artist} - {song_data.title} successfully save in {song_data.album}')

    def start(self, directory: Path) -> None:
        """Основная выполняющая функция, которая рекурсивно пробегается по всем файлам в directory и изменяет их"""
        from db.db_controller import DBController
        db = DBController()
        db.clear_table()

        for file_path in directory.iterdir():
            if file_path.is_dir():
                self.start(file_path)
            elif file_path.is_file() and file_path.suffix != '.jpg':
                song_data = self.get_info_from_file(file_path)
                db.insert(song_data)
                self.change_tags(song_data)

        self.delete_images(self.target_dir)


if __name__ == '__main__':
    from logger import set_up_logger_config
    set_up_logger_config()

    a = TagChanger('C:\\code\\tag_changer\\test_tag_change', ['Legend'])
    a.start(a.target_dir)

    # проверки и возможные функции для вычисления или извлечения данных
    # logger = logging.getLogger('TagChanger')
    # music = eyed3.load('C:\\code\\tag_changer\\test_tag_change\\'
    #                    'Legend\\Saint Asonia\\Flawed Design\\Saint Asonia,Sharon den Adel - Sirens.mp3')
    # logger.info(music.tag.images._fs[b'APIC'][0].picture_type)
