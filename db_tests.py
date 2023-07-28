import logging
import sys
from pathlib import Path
import eyed3

import db_controller as db

# todo доделать логи, переместить в отдельный файл
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s %(levelname)s] %(message)s'))
log.addHandler(handler)

client, mydb, collections = db.db_connection()
music_collection = collections['music_collection']
users_collection = collections['users_collection']
libraries_collection = collections['libraries_collection']

# Windows
SOURCE_DIR = Path('C:\\Users\\IvanK\\Music\\Music')
TARGET_DIR = Path('C:\\Users\\IvanK\\Music\\target_dir')
# Linux
SOURCE_DIR = Path('/home/lenex/code/tag_changeer/source_dir')
TARGET_DIR = Path('/home/lenex/code/tag_changeer/target_dir')


def load_data_to_db(directory: Path, core_directory: Path) -> None:
    for file in directory.iterdir():
        if file.is_dir():
            load_data_to_db(file, core_directory)
        elif file.is_file():
            file_relative_position = file.relative_to(core_directory)
            song = eyed3.load(file)
            try:
                title = song.tag.title
                artist = song.tag.artist
                album = song.tag.album
                if list(song.tag.images) and song.tag.images[0].image_data:
                    image = True
                else:
                    image = False
            except Exception as err:
                log.error(f'Error: {err.__class__.__name__}. Can`t read parameter in file {file}.')
                continue

            _load_data_to_db(core_directory, file_relative_position, title, artist, album, image)


def find_duplicates():
    duplicates = db.find_duplicates(music_collection)
    if not duplicates:
        print(f'There are no duplicates in {TARGET_DIR}')

    for duplicate in duplicates:
        for artist, title in duplicate.values():
            elements = db.find_document(
                music_collection,
                {'$and': [{'title': title}, {'artist': artist}]},
                {'file_path': 1, '_id': 0},
                multiple=True
            )

            print(f'{artist} - {title}')
            for i in range(len(elements)):
                print(f'{i + 1}. {elements[i]["file_path"]}')

            success = False
            while not success:
                elements_to_delete = input('\nEnter the numbers of elements you want to delete (in format 1 2 3) or 0 to console: ')

                try:
                    elements_to_delete = list(map(int, elements_to_delete.split()))
                except ValueError:
                    print(f'ValueError. You enter not numbers or not in write format')
                    continue

                if 0 in elements_to_delete:
                    print('Consoled\n')
                    break

                for e in elements_to_delete:
                    if e - 1 not in range(len(elements)):
                        print(f'Index {e} out of range')
                        break
                else:
                    success = True
                if not success:
                    continue

                for e in elements_to_delete:
                    db.delete_document(music_collection, {'file_path': elements[e - 1]['file_path']})
                    Path(TARGET_DIR, elements[e - 1]['file_path']).unlink()
                    print(f'{elements[e - 1]["file_path"]} was deleted')
                print()

                success = True


def synchronization(dir1, dir2):
    pass


def _load_data_to_db(library, file_path, title, artist, album, image):
    new_data = {
        'library': str(library),
        'file_path': str(file_path),
        'title': title,
        'artist': artist,
        'album': album,
        'image': image,
        'valid': False
    }
    # TODO
    '''
        Попробовать решить проблему синхронизации через поле валидности (уникальности)
        
        Изначально при записи в БД - файл невалидный (мб уникальный). Тогда же проверяется, есть ли в БД такой же файл
        в другой библиотеке. Если есть - файл валидный, если нет - так и остаётся невалидным.
        
        Вначале при изменении - находится такой же файл в другой библиотеке и становится невалидным. В конце изменения -
        изменяемый файл проходит процедуру валидацию, его "прошлый близнец" не проходит. "Близнец" может стать валидным,
        только если изменяемый файл остался таким же, или в последующем появился другой файл, способный стать его 
        "близнецом".
        
        При синхронизации искать в двух библиотеках (мб перед этим обновить их валидность в обоих библиотеках) все
        невалидные файлы и решать, что с ними делать.
    '''
    if db.find_document(music_collection, {'file_path': str(file_path), 'library': str(library)}):
        db.update_document(music_collection, {'file_path': str(file_path), 'library': str(library)}, new_data)
        log.info(f'{artist} - {title} updated')
    else:
        db.insert_document(music_collection, new_data)
        log.info(f'{artist} - {title} added to {library}')


if __name__ == '__main__':
    load_data_to_db(SOURCE_DIR, SOURCE_DIR)
    load_data_to_db(TARGET_DIR, TARGET_DIR)
    # find_duplicates()