import logging
from pathlib import Path
import re

import eyed3

from db import DBController
from model import SongData


# TODO:
#     * Посмотреть библиотеки для парсинга и почитать о
#     компиляторах, возможно получится упростить процедуру
#     обработки имён фалов.
#     * Поработать с изображениями. Сейчас они либо шакалятся,
#     либо берутся чёрт-пойми-откуда, либо ещё чего =(
class TagChanger:
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.target_dir = None
        self.artist_dirs = None

        # цифры + скобки|пробелы|точки|прочее
        self.pattern_to_number = re.compile(r'^\d+(\W | \W | |\)|\) )')
        # feat
        self.pattern_to_feat = re.compile(r'(\(|\s)(feat|Feat|ft|Ft)(\. |\.| )(?P<feats>.*?)(\)|$)')
        # опенинги/эндинги
        # TODO: в будущем мб можно сделать под кастомные запросы
        self.pattern_to_special = re.compile(r'\((OP|EN)(\d? |\d).*?\)')
        # мусорные скобки
        self.pattern_to_brackets = re.compile(r'([(\[].*?[)\]])(?![\s$]?\w)')
        self.logger.debug('Класс для работы с тэгами инициализирован')

    def delete_numbers(self, target: str) -> str:
        """Удаление цифр в начале"""
        target = self.pattern_to_number.sub('', target)
        self.logger.debug(f'del_num: {target=}')
        return target

    def split_fullname(self, target: str) -> [str, str]:
        """Разделение на artist, title"""
        try:
            artist, title = target.split(' - ')
        except ValueError:
            artist = ''
            title = target
        self.logger.debug(f'split_name: {artist=}, {title=}')
        return artist, title

    def split_artist(self, target: str) -> [str, list]:
        """Разделение артистов, что идут через запятую"""
        target = target.split(',')
        feat = [s.strip() for s in target]
        artist = feat.pop(0)
        self.logger.debug(f'split_artist: {artist=}, {feat=}')
        return artist, feat

    # TODO: мб добавить '&' (Artist & OtherArtist - Title)
    def find_feats(self, target: str) -> [str, list]:
        """Поиск соисполнителей в title и в artist"""
        feat = []
        match = self.pattern_to_feat.search(target)
        if match:
            # self.logger.debug(f'{match.group()}, {match.group("feats")=}')
            target = target.replace(match.group(), '').strip()
            feat = match.group('feats').split(',')
            feat = [feat.strip() for feat in feat]

        self.logger.debug(f'feats: {target=}, {feat=}')
        return target, feat

    def find_special(self, target: str) -> [str, str]:
        """Поиск опенингов/эндингов в title"""
        special = ''
        match = self.pattern_to_special.search(target)
        if match:
            special = match.group()
            target = target.replace(special, '').strip()

        self.logger.debug(f'special: {target=}, {special=}')
        return target, special

    def delete_brackets(self, target: str) -> str:
        """Удаление мусорных скобок"""
        target = self.pattern_to_brackets.sub('', target).strip()
        self.logger.debug(f'brackets: {target=}')
        return target

    @staticmethod
    def merge(title: str, feat: str, special: str) -> str:
        """Соединение title, feat и special воедино"""
        return ' '.join(list(i for i in (title, f'(feat. {feat})' if feat else '', special) if i))

    def get_image(self, file_dir: Path, album: str) -> Path | None:
        """
        Нахождение обложки по пути и названию альбома.
        Если такой нет - создаёт и возращает из первого файла с картинкой.
        Если и это не получается - возвращает None.
        """
        self.logger.debug(f'Попытка получить обложку: {file_dir}, {album}')
        images = list(file_dir.glob('*.jpg'))
        image_path = Path(file_dir, album + '.jpg')

        if images:
            image = images[0]
            if image.stem != album:
                image.rename(image_path)
            self.logger.debug(f'Обложка получена из файла: "{str(image_path)}"')
            return image_path
        else:
            for file_path in file_dir.iterdir():
                try:
                    song = eyed3.load(file_path)
                    image = song.tag.images[0].image_data
                    with open(image_path, 'wb+') as album_cover:
                        album_cover.write(image)
                    self.logger.debug(f'Обложка создана из файла: "{str(file_path)}"')
                    return image_path
                except IndexError:
                    self.logger.debug(f'Аудиофайл без обложки: "{file_path}"')
                    continue
                except AttributeError:
                    # INFO: может вызваться, когда у song вообще нет тегов images
                    # self.logger.error(f'Unknown error: {e}')
                    continue
                except OSError:
                    self.logger.debug(f'Невозможно прочитать файл: "{file_path}"')
                    continue

        self.logger.debug('Обложку найти не удалось')
        return None

    def delete_images(self, target_dir: Path) -> None:
        """Удаляет все изображения из target_dir за исключением 'помеченных'"""
        # TODO: удалять надо после того как функция закончилась.
        # Она рекурсивная, а вызывает каждый раз с глобальной переменной
        for file in target_dir.iterdir():
            if file.is_dir():
                self.delete_images(file)
            elif file.suffix == '.jpg' and file.parent.name not in ['The Best', 'Nirvana', 'OSU']:
                self.logger.debug(f'Удаление обложки: "{file}"')
                file.unlink()

    def get_info_from_file(self, file_path: Path) -> SongData:
        """
        Достаёт всю информацию из аудиофайла по пути file_path.
        При level=3 изменяет путь до файла.
        Записывает и возвращает все данные в виде SongData.
        """
        self.logger.debug(f'Получение информации: {file_path.stem}')

        # INFO: level
        #     1 - просто в папке, 2 - в папке с альбомом,
        #     3 - исполнитель без альбома, 4 - исполнитель с альбомом.
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
        feat = ', '.join(feat1 + feat2 + feat3)
        title, special = self.find_special(title)
        title = self.delete_brackets(title)

        song = eyed3.load(file_path)

        if level == 1:
            # просто в папке (как в the best)
            album = relative_path.parts[0]
        elif level == 2:
            # в папке с альбомом
            album = relative_path.parts[1]
        elif level == 3:
            # в исполнителе без альбома (создаётся папка с альбомом)
            try:
                album = song.tag.album
            except AttributeError:
                album = 'Without Album'
            album_dir = Path(file_path.parent, album)
            album_dir.mkdir(parents=True, exist_ok=True)
            file_path = file_path.replace(Path(album_dir, file_path.name))
            relative_path = file_path.relative_to(self.target_dir)
            artist = relative_path.parts[1]
        else:
            # в исполнителе с альбомом
            artist = relative_path.parts[1]
            album = relative_path.parts[2]

        image = self.get_image(file_path.parent, album)
        return SongData(relative_path, title, artist, album, feat, special, image)

    def change_tags(self, song_data: SongData) -> None:
        """
        Сначала стирает все id3 tag из файла,
        а потом записывает новыми, взятыми из song_data
        """
        file_path = Path(self.target_dir, song_data.file_path)
        self.logger.debug(f'Обработка файла "{file_path}"')
        song = eyed3.load(file_path)
        song.initTag()
        song.tag.remove(file_path)

        title = self.merge(song_data.title, song_data.feat, song_data.special)
        song.tag.title = title
        song.tag.artist = song_data.artist
        song.tag.album = song_data.album
        if song_data.image:
            with open(song_data.image, "rb") as image:
                # TODO: вот тут надо как-то понять,
                #   где картинки шакалятся и как они вообще храняться?
                song.tag.images.set(3, image.read(), "image/jpeg")
        song.tag.save()
        # PERF: а это зачем? может всё же не надо в бд картинки хранить?
        #   Оно как бы понятно, что вот у тебя был полный путь до обложки,
        #   а теперь обрезанный, что бы в бд запхать, но мы их всё равно удаляем.
        #   Если не хранить картинку в бинарной форме или где-то на
        #   удалённом сервере, и уже там путь указывать, то
        #   сохранять обложки в бд - смысла нет.
        if song_data.image is not None:
            song_data.image = song_data.image.relative_to(self.target_dir)
        self.logger.info(f'[{song_data.album:^20}] [{song_data.artist:^20}] [{song_data.title:^20}]')

    def start(self, directory: Path):
        """
        Основная выполняющая функция, которая рекурсивно
        пробегается по всем файлам в directory и изменяет их
        """
        # TODO: может сделать не генератом а созданием тасков?
        #     чтобы потом и в бд можно было закинуть колбэком
        #     и посчитать, сколько задачь стоит для прогресс бара
        #     при этом не сильно тратится на выделение памяти для 4000 песен
        for file_path in directory.iterdir():
            if file_path.is_dir():
                yield from self.start(file_path)
            elif file_path.is_file() and file_path.suffix != '.jpg':
                song_data = self.get_info_from_file(file_path)
                self.change_tags(song_data)
                yield song_data


def main_linux() -> None:
    tc = TagChanger()
    tc.target_dir = Path('/home/lenex/code/tag_changer/test_target_dir/')
    tc.artist_dirs = ['Legend', 'Легенды']
    items = tc.start(tc.target_dir)
    for song_data in items:
        pass
    tc.delete_images(tc.target_dir)


def main_wind() -> None:
    a = TagChanger()
    a.target_dir = 'C:\\code\\tag_changer\\test_target_dir'
    a.artist_dirs = ['Legend', 'Легенды']
    items = a.start(a.target_dir)

    with DBController() as db:
        db.create_table_if_not_exist('test_main')
        for item in items:
            db.insert(item, 'test_main')


def test_linux() -> None:
    # проверки и возможные функции для вычисления или извлечения данных
    file_path = '/home/lenex/code/tag_changer/test_target_dir/Legend/Saint Asonia/Saint Asonia - Weak & Tired.mp3'
    song = eyed3.load(file_path)
    song.tag.remove(file_path)


def test_wind() -> None:
    # file_path = 'C:\\code\\tag_changer\\test_tag_change\\Legend\\Saint Asonia\\Flawed Design\\Saint Asonia,Sharon den Adel - Sirens.mp3'
    pass


def test_img() -> None:
    file_path = '/home/lenex/code/tag_changer/test_target_dir/Legend/Saint Asonia/Saint Asonia - Weak & Tired.mp3'
    song = eyed3.load(file_path)
    song.initTag()
    print(song.tag.images._fs[b'APIC'][0].picture_type)

    image = song.tag.images[0].image_data
    image_path = '/home/lenex/code/tag_changer/test_target_dir/Legend/Saint Asonia/cover2.jpg'
    with open(image_path, 'wb+') as album_cover:
        album_cover.write(image)


if __name__ == '__main__':
    from logger import set_up_logger_config
    set_up_logger_config()

    main_linux()
    # main_wind()
    # test_wind()
    # test_linux()
    # test_img()

