# TODO
#  - мб придумать для каждой такой диры обложку и загрузить в исходник
#  - добавить инфы в папки
#  - сделать что-то с копированием. пока что данная реализация не нужна. по сути нужен запуск скрипта в source, после
#  чего ручками перекидывать в target. было бы здорово работать сразу в target.

import re
import eyed3
from eyed3.core import AudioFile
from pathlib import Path

from utils.logger import log
from utils.model import MusicData

# избавляет от скобок
PATTERN_TO_NAME = re.compile(r'\s?\((?!(feat|ft|Feat|Ft|OP|EN)(\s|\.|\d+)).*\)$')
# избавляет от цифр в начале
PATTERN_TO_NUMBER = re.compile(r'(^\d+(\W | \W | |\)))', re.MULTILINE)
# паттерн для feat
PATTERN_TO_FEAT = re.compile(r'(\(|\s)(feat|ft|Feat|Ft)(\.|\s)(.*?)(\)?$)')


def create_image(file_dir: Path, album: str) -> Path | None:
    images = list(file_dir.glob('*.jpg'))
    if images:
        image = images[0]
        if image.stem != album:
            image = image.rename(Path(file_dir, album + '.jpg'))
        return image
    else:
        for file_path in file_dir.iterdir():
            song = eyed3.load(file_path)
            try:
                image = song.tag.images[0].image_data
            except IndexError:
                image = None
            except AttributeError:
                image = None
            if image:
                with open(Path(file_dir, album + '.jpg'), 'wb+') as album_cover:
                    album_cover.write(image)
                log.info(f'Create image {Path(file_dir, album + ".jpg")}')
                return Path(file_dir, album + '.jpg')
            else:
                return None


def delete_images(target_dir: Path) -> None:
    images = target_dir.glob('**/*.jpg')
    for image in images:
        log.info(f'Delete image {image}')
        image.unlink()


def add_tags(song: AudioFile, song_data: MusicData, level: int) -> None:
    log.debug(f'{"---" * level}>[{song_data.artist}, {song_data.title}, {song_data.album}]')
    song.initTag()
    song.tag.remove(song_data.file_path)

    song.tag.title = song_data.title
    song.tag.artist = song_data.artist
    song.tag.album = song_data.album

    if song_data.image:
        with open(song_data.image, "rb") as image:
            song.tag.images.set(3, image.read(), "image/jpeg")

    song.tag.save()
    log.info(f'{song_data.artist} - {song_data.title} successfully save in {song_data.album}')


def prepare_name(file: Path) -> tuple[list[str], str]:
    name = file.stem
    name = re.sub(PATTERN_TO_NAME, '', name)
    name = PATTERN_TO_NAME.sub('', name)
    name = PATTERN_TO_NUMBER.sub('', name)
    name = name.split(' - ')

    if len(name) > 1:
        title = name[1]
    else:
        title = name[0]

    return name, title


def change_feat(title: str, artist: str) -> [str, str]:
    try:
        feat = PATTERN_TO_FEAT.split(title)
        title = feat[0].strip()
        feat = feat[4].strip()
    except IndexError:
        feat = ''

    if len(artist.split(',')) > 1:
        feat = f'{feat + ", " if feat else ""}' + ', '.join(map(lambda a: a.strip(), artist.split(',')[1:]))
        artist = artist.split(',')[0].strip()
    if feat:
        title = title + f' (feat. {feat})'

    return title, artist


def tag_change(core_dir: Path, target_dir: Path, artist_dirs: list[str]) -> None:
    """
    Основная функция, рекурсивно обрабатывает файлы в target_dir относительно core_dir. Файлы в artist_dirs
    обрабатываются по особому паттерну.

    :param core_dir: неизменная директория относительно которой обрабатывается target_dir.
    :param target_dir: текущая директория, меняется соответственно уровню погружения.
    :param artist_dirs: список с особыми директориями.
    :return: None
    """

    for file_path in target_dir.iterdir():
        file = file_path.relative_to(core_dir)
        level = len(file.parts) - 1

        if file_path.is_dir():
            log.debug(f'{"---" * level}{file.name}')
            tag_change(core_dir, file_path, artist_dirs)

        elif file_path.is_file() and file.suffix != '.jpg':
            song_data = MusicData(file_path=file_path)
            name, song_data.title = prepare_name(file)
            song = eyed3.load(file_path)

            # Нужно для песен в исполнителе без альбома (создаётся папка с альбомом) (см. level == 2, ARTIST_DIRS)
            try:
                song_data.album = song.tag.album
            except AttributeError:
                song_data.album = ''

            # песни в директориях (как в the best)
            if level == 1:
                song_data.artist = name[0]
                song_data.album = file.parts[0]
                song_data.image = None  # TODO пока что не добавлять картинки в обычные папки. Изменить после доработки БД.

            # песни в директориях и в альбоме
            elif level == 2:
                # песни в исполнителе без альбома (создаётся папка с альбомом)
                if file.parts[0] in artist_dirs:
                    Path(file_path.parent, song_data.album).mkdir(parents=True, exist_ok=True)
                    song_data.file_path = file_path.replace(Path(file_path.parent, song_data.album, file.name))
                    song_data.artist = file.parts[1]
                    song_data.image = create_image(song_data.file_path.parent, song_data.album)
                    add_tags(eyed3.load(song_data.file_path), song_data, level)
                    continue
                song_data.artist = name[0]
                song_data.album = file.parts[1]
                song_data.image = create_image(file_path.parent, song_data.album)

            # песни в исполнителях в альбомах (level == 3)
            else:
                song_data.artist = file.parts[1]
                song_data.album = file.parts[2]
                song_data.image = create_image(file_path.parent, song_data.album)

            song_data.title, song_data.artist = change_feat(song_data.title, song_data.artist)
            add_tags(song, song_data, level)


ARTIST_DIRS = ['Legend', 'Легенды']
# Windows
SOURCE_DIR = Path('C:\\Users\\IvanK\\Music\\Music')
TARGET_DIR = Path('C:\\Users\\IvanK\\Music\\target_dir')
# Linux
SOURCE_DIR = Path('../source_dir')
TARGET_DIR = Path('../target_dir')
'''
settings.txt

SOURCE_DIR=/home/lenex/code/tag_changeer/target_dir -------- C:/Code/tag_changer/target_dir
ARTIST_DIRS=Legend, Легенды
'''

if __name__ == '__main__':
    tag_change(TARGET_DIR, TARGET_DIR, ARTIST_DIRS)
    print('\n')
    delete_images(TARGET_DIR)
