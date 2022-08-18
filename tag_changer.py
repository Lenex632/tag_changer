from pathlib import Path
import re
import eyed3
import shutil

SOURCE_DIR = Path(Path.cwd(), 'test_tag_change')
TARGET_DIR = Path(Path.cwd(), 'target_dir')

EXT_TO_SEARCH = ['.mp3', '.m4a']
ARTIST_DIRS = ['`Legend', '`Легенды']

# избавляет от скобок
PATTERN_TO_NAME = re.compile(r'\s?\((?!feat|OP).*\)')
# избавляет от цифр в начале
PATTERN_TO_NUMBER = re.compile(r'(\d*\s?[.-]?\s?)?(.+)')

datas = []

print('copying...')
shutil.rmtree(TARGET_DIR, ignore_errors=True)
shutil.copytree(SOURCE_DIR, TARGET_DIR)


def tag_change(target_dir):
    for file in target_dir.iterdir():
        if file.is_dir():
            datas.append(file.name)
            tag_change(file)
        elif file.is_file():
            datas.append(file.name)

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
print(datas)

