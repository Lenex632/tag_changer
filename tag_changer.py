# TODO
#  - мб придумать для каждой такой диры обложку и загрузить в исходник
#  - добавить инфы в папки
#  - сделать что-то с копированием. пока что данная реализация не нужна. по сути нужен запуск скрипта в source, после
#  чего ручками перекидывать в target. было бы здорово работать сразу в target.

from pathlib import Path
import re
import eyed3

from logger import log
from eyed3.core import AudioFile
from logger import log

# Windows
SOURCE_DIR = Path('C:\\Users\\IvanK\\Music\\Music')
TARGET_DIR = Path('C:\\Users\\IvanK\\Music\\target_dir')
# Linux
SOURCE_DIR = Path('/home/lenex/code/tag_changeer/test_tag_change')
TARGET_DIR = Path('/home/lenex/code/tag_changeer/target_dir')

ARTIST_DIRS = ['Legend', 'Легенды']

client, mydb, collections = db.db_connection()
music_collection = collections['music_collection']
users_collection = collections['users_collection']
libraries_collection = collections['libraries_collection']

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
        # TODO пошаманить тут (не очень нравится логика и структура)
        for file_path in file_dir.iterdir():
            song = eyed3.load(file_path)
            try:
                image = song.tag.images[0].image_data
            except IndexError:
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


def add_tags(song: AudioFile, file_path: Path, title: str, artist: str, album: str, image: Path, level: int) -> None:
    log.debug(f'{"---" * level}>[{artist}, {title}, {album}]')
    song.initTag()
    song.tag.remove(file_path)

    song.tag.title = title
    song.tag.artist = artist
    song.tag.album = album

    if image:
        with open(image, "rb") as image:
            song.tag.images.set(3, image.read(), "image/jpeg")

    song.tag.save()
    log.info(f'{artist} - {title} successfully save in {album}')


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
            name, title = prepare_name(file)
            song = eyed3.load(file_path)

            # Нужно для песен в исполнителе без альбома (создаётся папка с альбомом) (см. level == 2, ARTIST_DIRS)
            # TODO не появляется на тестах
            try:
                album = song.tag.album
            except:
                album = ''

            # песни в директориях (как в the best)
            if level == 1:
                artist = name[0]
                album = file.parts[0]
                image = None  # TODO пока что не добавлять картинки в обычные папки. Изменить после доработки БД.

            # песни в директориях и в альбоме
            elif level == 2:
                # песни в исполнителе без альбома (создаётся папка с альбомом)
                if file.parts[0] in artist_dirs:
                    Path(file_path.parent, album).mkdir(parents=True, exist_ok=True)
                    new_file_path = file_path.replace(Path(file_path.parent, album, file.name))
                    artist = file.parts[1]
                    image = create_image(new_file_path.parent, album)
                    add_tags(eyed3.load(new_file_path), new_file_path, title, artist, album, image, level)
                    continue
                artist = name[0]
                album = file.parts[1]
                image = create_image(file_path.parent, album)

            # песни в исполнителях в альбомах (level == 3)
            else:
                artist = file.parts[1]
                album = file.parts[2]
                image = create_image(file_path.parent, album)

            title, artist = change_feat(title, artist)
            add_tags(song, file_path, title, artist, album, image, level)


if __name__ == '__main__':
    '''
    settings.txt
    
    SOURCE_DIR=/home/lenex/code/tag_changeer/target_dir -------- C:/Code/tag_changer/target_dir
    ARTIST_DIRS=Legend, Легенды
    '''

    # Windows
    SOURCE_DIR = Path('C:\\Users\\IvanK\\Music\\Music')
    TARGET_DIR = Path('C:\\Users\\IvanK\\Music\\target_dir')
    # Linux
    SOURCE_DIR = Path('/home/lenex/code/tag_changeer/test_tag_change')
    TARGET_DIR = Path('/home/lenex/code/tag_changeer/target_dir')

    ARTIST_DIRS = ['Legend', 'Легенды']

    tag_change(TARGET_DIR, TARGET_DIR, ARTIST_DIRS)
    print('\n')
    delete_images(TARGET_DIR)
