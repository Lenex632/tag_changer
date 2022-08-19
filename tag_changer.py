from pathlib import Path
import re
import eyed3
import shutil

SOURCE_DIR = Path(Path.cwd(), 'test_tag_change')
TARGET_DIR = Path(Path.cwd(), 'target_dir')

EXT_TO_SEARCH = ['.mp3', '.m4a']
ARTIST_DIRS = ['`Legends', '`Легенды']

# избавляет от скобок
PATTERN_TO_NAME = re.compile(r'\s?\((?!feat|OP).*\)')
# избавляет от цифр в начале
PATTERN_TO_NUMBER = re.compile(r'(^\d+\s?\W?\s?)(?!$)')


print('copying...')
shutil.rmtree(TARGET_DIR, ignore_errors=True)
shutil.copytree(SOURCE_DIR, TARGET_DIR)


def tag_change(target_dir):
    for file_path in target_dir.iterdir():
        file = file_path.relative_to(TARGET_DIR)
        level = len(file.parts)
        if file_path.is_dir():
            print('---'*(level-1), file.name)
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

            if level == 2:
                artist = name[0]
                title = name[1]
                album = file.parts[0]
                print('---' * (level - 1) + '>', [artist, title, album])
            if level == 3:
                if file.parts[0] in ARTIST_DIRS:
                    Path(file_path.parent, album).mkdir(parents=True, exist_ok=True)
                    file_path.replace(Path(file_path.parent, album, file.name))
                    artist = file.parts[1]
                    title = name[1]
                    print('---' * (level - 1) + '>', [artist, title, album])
                    continue
                artist = name[0]
                title = name[1]
                album = file.parts[1]
                print('---' * (level - 1) + '>', [artist, title, album])
            if level == 4:
                artist = file.parts[1]
                title = name[0]
                album = file.parts[2]
                print('---' * (level - 1) + '>', [artist, title, album])

# def tag_change(source_dir: Path, target_dir: Path):
#     for path_to_file in target_dir.iterdir():
#         file = path_to_file.relative_to(target_dir)
#         flag = False
#
#         # определяет что папка с артистами
#         if file.parts[0] in ARTIST_DIRS:
#             flag = True
#         # определяет на каком уровне рассматривать файлы
#         level = len(file.parts) - 1 + flag
#
#         if path_to_file.is_dir():
#             tag_change(path_to_file)
#         elif file.suffix in EXT_TO_SEARCH:
#
#             song = eyed3.load(path_to_file)
#
#             # получить альбом и обложку для песни в дирах в исполнителях
#             try:
#                 album = song.tag.album
#                 image = song.tag.images[0].image_data
#                 path_to_image = Path(path_to_file.parent, f'{album}.jpg')
#             except:
#                 album = ''
#                 image = ''
#                 path_to_image = ''
#
#             song.initTag()
#             song.tag.remove(path_to_file)
#
#             # разбивает имя на части
#             name_parts = file.stem.split(' - ')
#             # разбивает путь на части
#             path_parts = file.parts
#
#             try:
#                 title = name_parts[1]
#             except:
#                 title = file.stem
#             title = re.sub(PATTERN_TO_NAME, '', title)
#             title = re.match(PATTERN_TO_NUMBER, title).group(2)
#             song.tag.title = title
#             # песни в дирах
#             if level == 1:
#                 song.tag.artist = re.match(PATTERN_TO_NUMBER, name_parts[0]).group(2)
#                 song.tag.album = path_parts[0]  # TODO или вообще удалить
#             # песни в дирах в альбомах
#             elif level == 2:
#                 song.tag.artist = re.match(PATTERN_TO_NUMBER, name_parts[0]).group(2)
#                 song.tag.album = path_parts[1]
#
#                 path_to_image = list(path_to_file.parent.glob('*.jpg'))
#                 if path_to_image:
#                     with open(path_to_image[0], "rb") as image:
#                         song.tag.images.set(3, image.read(), "image/jpeg")
#             # песни в дирах в исполнителях
#             elif level == 3:
#                 song.tag.artist = path_parts[1]
#                 song.tag.album = album
#
#                 if path_to_image:
#                     with open(path_to_image, 'wb+') as album_cover:
#                         album_cover.write(image)
#                     with open(path_to_image, 'rb') as image:
#                         song.tag.images.set(3, image.read(), "image/jpeg")
#                 path_to_image.unlink()
#             # песни в дирах в исполнителях в альбомах
#             elif level == 4:
#                 song.tag.artist = path_parts[1]
#                 song.tag.album = path_parts[2]
#
#                 path_to_image = list(path_to_file.parent.glob('*.jpg'))
#                 if path_to_image:
#                     with open(path_to_image[0], "rb") as image:
#                         song.tag.images.set(3, image.read(), "image/jpeg")
#
#             song.tag.save()
#             print('---' * (level - 1) + '>', file)


tag_change(TARGET_DIR)
