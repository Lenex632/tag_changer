from pathlib import Path
import re
import eyed3
import shutil

SOURCE_DIR = Path(Path.cwd(), 'test_tag_change')
TARGET_DIR = Path(Path.cwd(), 'target_dir')
DATA_FILE = Path(Path.cwd(), 'data.txt')

ARTIST_DIRS = ['`Legends', '`Legend', '`Легенды', 'Legends', 'Legend', 'Легенды']

# TODO что-то придумать с названиями из цифр + множественные исполнители через запятую
# избавляет от скобок
PATTERN_TO_NAME = re.compile(r'\s?\((?!feat|OP).*\)')
# избавляет от цифр в начале
PATTERN_TO_NUMBER = re.compile(r'(^\d+\s?\W?\s?)(?!$)')

print('creation data.txt\n')
DATA_FILE.unlink(missing_ok=True)
DATA_FILE.touch(exist_ok=True)
print('copying...\n')
shutil.rmtree(TARGET_DIR, ignore_errors=True)
shutil.copytree(SOURCE_DIR, TARGET_DIR)


def create_image(file_dir, album):
    images = list(file_dir.glob('*.jpg'))
    if images:
        image = images[0]
        if image.stem != album:
            image = image.rename(Path(file_dir, album+'.jpg'))
        return image
    else:
        for file_path in file_dir.iterdir():
            song = eyed3.load(file_path)
            try:
                image = song.tag.images[0].image_data
            except:
                image = None
                return image
            if image:
                with open(Path(file_dir, album+'.jpg'), 'wb+') as album_cover:
                    album_cover.write(image)
                return Path(file_dir, album+'.jpg')


def write_data_file(file, level, artist, title, album, image):
    print('---' * level + '>', [artist, title, album])
    DATA_FILE.open(mode='a+').write(f'{file}\n'
                                    f'   title: {title}\n'
                                    f'   artist: {artist}\n'
                                    f'   album: {album}\n'
                                    f'   image: {image}\n\n')


def delete_images(target_dir):
    images = target_dir.glob('**/*.jpg')
    for image in images:
        print(f'Delete image {image}')
        image.unlink()


def add_tags(song, file_path, title, artist, album, image):
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
        elif file_path.is_file():
            name = file.stem
            name = re.sub(PATTERN_TO_NAME, '', name)
            name = re.sub(PATTERN_TO_NUMBER, '', name, re.MULTILINE)
            name = name.split(' - ')

            song = eyed3.load(file_path)
            try:
                album = song.tag.album
            except:
                album = ''

            # песни в дирах (как в the best)
            # TODO мб придумать для каждой такой диры обложку и загрузить в исходник
            if level == 1:
                title = name[1]
                artist = name[0]
                album = file.parts[0]
                image = None
                add_tags(song, file_path, title, artist, album, image)
            # песни в дирах и в альбоме
            elif level == 2:
                # песни в исполнителе без альбома (создаётся папка с альбомом)
                if file.parts[0] in ARTIST_DIRS:
                    Path(file_path.parent, album).mkdir(parents=True, exist_ok=True)
                    new_file_path = file_path.replace(Path(file_path.parent, album, file.name))
                    artist = file.parts[1]
                    title = name[1]
                    image = create_image(new_file_path.parent, album)
                    add_tags(eyed3.load(new_file_path), new_file_path, title, artist, album, image)
                    write_data_file(new_file_path.relative_to(TARGET_DIR), level, artist, title, album, image)
                    continue
                title = name[1]
                artist = name[0]
                album = file.parts[1]
                image = create_image(file_path.parent, album)
            # песни в исполнителях в альбомах (level=3)
            else:
                artist = file.parts[1]
                title = name[0]
                album = file.parts[2]
                image = create_image(file_path.parent, album)
            add_tags(song, file_path, title, artist, album, image)
            write_data_file(file, level, artist, title, album, image)


tag_change(TARGET_DIR)
print('\n')
delete_images(TARGET_DIR)
