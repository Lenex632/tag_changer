# добавить инфы в папки
# F:\Music\target_dir\The Best\Brutal Legend
# F:\Music\target_dir\Legend\Green Day\DOS
# F:\Music\target_dir\Legend\Green Day\Insomniac
# F:\Music\target_dir\Legend\Green Day\Tre
# F:\Music\target_dir\Legend\Green Day\UNO
from pathlib import Path
import re
import eyed3
import shutil
import pandas as pd

# Windows
SOURCE_DIR = Path('/mnt/f/Music/source_dir')
TARGET_DIR = Path('/mnt/f/Music/target_dir')
# Linux
SOURCE_DIR = Path('/home/lenex/code/tag_changeer/test_tag_change')
TARGET_DIR = Path('/home/lenex/code/tag_changeer/target_dir')

# DATA_FILE = Path(Path.cwd(), 'data.xlsx')
# DATA_FILE_COMPARE = Path(Path.cwd(), 'data_compare.xlsx')

data_list = []  # todo

ARTIST_DIRS = ['`Legends', '`Legend', '`Легенды', 'Legends', 'Legend', 'Легенды']

# избавляет от скобок
PATTERN_TO_NAME = re.compile(r'\s?\((?!feat|ft|OP|EN).*\)')
# избавляет от цифр в начале
PATTERN_TO_NUMBER = re.compile(r'(^\d+(\W | \W | ))')
PATTERN_TO_FEAT = re.compile(r'(feat|ft)\.?\s?')

# todo что-то придумать с копированием/переносом/пересозданием
# print('copying...\n')
# shutil.rmtree(TARGET_DIR, ignore_errors=True)
# shutil.copytree(SOURCE_DIR, TARGET_DIR)


def create_image(file_dir, album):
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
            except:
                image = None
            if image:
                with open(Path(file_dir, album + '.jpg'), 'wb+') as album_cover:
                    album_cover.write(image)
                return Path(file_dir, album + '.jpg')
            else:
                return image


def delete_images(target_dir):
    images = target_dir.glob('**/*.jpg')
    for image in images:
        print(f'Delete image {image}')
        image.unlink()


def add_tags(song, file_path, title, artist, album, image, level):
    data_list.append((file_path, artist, title, album, image))
    print('---' * level + '>', [artist, title, album])

    song.initTag()
    song.tag.remove(file_path)

    song.tag.title = title
    song.tag.artist = artist
    song.tag.album = album

    if image:
        with open(image, "rb") as image:
            song.tag.images.set(3, image.read(), "image/jpeg")

    song.tag.save()


def tag_change(target_dir):
    for file_path in target_dir.iterdir():
        file = file_path.relative_to(TARGET_DIR)
        level = len(file.parts) - 1
        if file_path.is_dir():
            print(f'{"---" * level}{file.name}')
            tag_change(file_path)
        # todo не обробатывать img
        elif file_path.is_file():
            name = file.stem
            name = re.sub(PATTERN_TO_NAME, '', name)
            name = re.sub(PATTERN_TO_NUMBER, '', name, re.MULTILINE)
            name = name.split(' - ')
            # todo доделать feat

            song = eyed3.load(file_path)
            # Нужно для песен в исполнителе без альбома (создаётся папка с альбомом) (см. level == 2, ARTIST_DIRS)
            try:
                album = song.tag.album
            except:
                album = ''

            # песни в дирах (как в the best)
            # TODO мб придумать для каждой такой диры обложку и загрузить в исходник
            if level == 1:
                # todo бахнуть ошибку
                title = name[1]
                artist = name[0]
                try:
                    feat = re.sub(PATTERN_TO_FEAT, '', title).split('(')[1][:-1]
                except:
                    feat = ''

                if len(artist.split(',')) > 1:
                    feat = f'{feat + ", " if feat else ""}' + ', '.join(map(lambda a: a.strip(), artist.split(',')))
                    # feat = feat + ', '.join(artist.split(','))
                    artist = artist.split(',')[0].strip()
                if feat:
                    title = title + f' ({feat})'
                album = file.parts[0]
                image = None
            # песни в дирах и в альбоме
            elif level == 2:
                # песни в исполнителе без альбома (создаётся папка с альбомом)
                if len(name) > 1:
                    title = name[1]
                else:
                    title = name[0]
                if file.parts[0] in ARTIST_DIRS:
                    Path(file_path.parent, album).mkdir(parents=True, exist_ok=True)
                    new_file_path = file_path.replace(Path(file_path.parent, album, file.name))
                    artist = file.parts[1]
                    image = create_image(new_file_path.parent, album)
                    add_tags(eyed3.load(new_file_path), new_file_path, title, artist, album, image, level)
                    continue
                artist = name[0]
                if len(artist.split(',')) > 1:
                    title = f'{title} (feat. {artist.split(",", maxsplit=1)[1].strip()})'
                    artist = artist.split(",")[0].strip()
                album = file.parts[1]
                image = create_image(file_path.parent, album)
            # песни в исполнителях в альбомах (level == 3)
            else:
                if len(name) > 1:
                    title = name[1]
                else:
                    title = name[0]
                artist = file.parts[1]
                album = file.parts[2]
                image = create_image(file_path.parent, album)
            add_tags(song, file_path, title, artist, album, image, level)


def analyze(dir1: Path, dir2: Path):
    data_1 = []
    data_2 = []
    go_through(dir1, dir1, data_1)
    go_through(dir2, dir2, data_2)
    data_copy = data_1.copy()
    for data in data_1:
        if data in data_2:
            data_copy.remove(data)
            data_2.remove(data)
    print(data_1)
    print(data_2)


def go_through(core: Path, directory: Path, data: list):
    for file in directory.iterdir():
        if file.is_dir():
            go_through(core, file, data)
        else:
            data.append(file.relative_to(core))


if __name__ == '__main__':
    tag_change(TARGET_DIR)
    print('\n')
    delete_images(TARGET_DIR)
    # files, artists, titles, albums, images = zip(*data_list)
    # df = pd.DataFrame({'file': files, 'artist': artists, 'title': titles, 'album': albums, 'image': images})
    # df.to_excel(DATA_FILE)

    # analyze(SOURCE_DIR, TARGET_DIR)

