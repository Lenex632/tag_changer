from pathlib import Path
import re
import eyed3

# tag_change_dir = Path('/mnt/d/Music/tag_change')
tag_change_dir = Path('/mnt/d/Music/test_tag_change2')

suffix_to_search = ['.mp3', '.m4a']
artist_dirs = ['`Legend', '`Легенды']

# избавляет от скобок
pattern_to_name = re.compile(r'\s?\((?!feat|OP).*\)')
# избавляет от цифр в начале
pattern_to_number = re.compile(r'(\d*\s?[.-]?\s?)?(.+)')


def tag_change(path: Path):
    for path_to_file in path.iterdir():
        file = path_to_file.relative_to(tag_change_dir)
        flag = False

        # определяет что папка с артистами
        if file.parts[0] in artist_dirs:
            flag = True
        # определяет на каком уровне рассматривать файлы
        level = len(file.parts) - 1 + flag

        if path_to_file.is_dir():
            tag_change(path_to_file)
        elif file.suffix in suffix_to_search:
            song = eyed3.load(path_to_file)

            # получить альбом и обложку для песни в дирах в исполнителях
            try:
                album = song.tag.album
                image = song.tag.images[0].image_data
                path_to_image = Path(path_to_file.parent, f'{album}.jpg')
            except:
                album = ''
                image = ''
                path_to_image = ''

            song.initTag()
            song.tag.remove(path_to_file)

            # разбивает имя на части
            name_parts = file.stem.split(' - ')
            # разбивает путь на части
            path_parts = file.parts

            try:
                title = name_parts[1]
            except:
                title = file.stem
            title = re.sub(pattern_to_name, '', title)
            title = re.match(pattern_to_number, title).group(2)
            song.tag.title = title
            # песни в дирах
            if level == 1:
                song.tag.artist = re.match(pattern_to_number, name_parts[0]).group(2)
                song.tag.album = path_parts[0]  # TODO или вообще удалить
            # песни в дирах в альбомах
            elif level == 2:
                song.tag.artist = re.match(pattern_to_number, name_parts[0]).group(2)
                song.tag.album = path_parts[1]

                path_to_image = list(path_to_file.parent.glob('*.jpg'))
                if path_to_image:
                    with open(path_to_image[0], "rb") as image:
                        song.tag.images.set(3, image.read(), "image/jpeg")
            # песни в дирах в исполнителях
            elif level == 3:
                song.tag.artist = path_parts[1]
                song.tag.album = album
                
                if path_to_image:
                    with open(path_to_image,'wb+') as album_cover:
                        album_cover.write(image)
                    with open(path_to_image, 'rb') as image:
                        song.tag.images.set(3, image.read(), "image/jpeg")
                path_to_image.unlink()
            # песни в дирах в исполнителях в альбомах
            elif level == 4:
                song.tag.artist = path_parts[1]
                song.tag.album = path_parts[2]

                path_to_image = list(path_to_file.parent.glob('*.jpg'))
                if path_to_image:
                    with open(path_to_image[0], "rb") as image:
                        song.tag.images.set(3, image.read(), "image/jpeg")

            song.tag.save()
            print('---' * (level - 1) + '>', file)


tag_change(tag_change_dir)
