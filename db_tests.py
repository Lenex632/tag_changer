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
SOURCE_DIR = Path('/home/lenex/code/tag_changeer/test_tag_change')
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
    for duplicate in duplicates:
        for artist, title in duplicate.values():
            elements = db.find_document(
                music_collection,
                {'$and': [{'title': title}, {'artist': artist}]},
                {'file_path': 1, '_id': 0},
                multiple=True
            )
            print()
            for element in elements:
                print(element['file_path'])
            print()
            for element in elements:
                print(element['file_path'])
                answer = None
                while answer not in ['y', 'n']:
                    answer = input('delete? [y/n] ')
                    match answer:
                        case 'y':
                            print('deleted')
                        case 'n':
                            print('save')
                        case _:
                            print('please enter y/n')


def _load_data_to_db(library, file_path, title, artist, album, image):
    if db.find_document(music_collection, {'file_path': str(file_path)}):
        db.update_document(
            music_collection,
            {'file_path': str(file_path)},
            {
                'library': str(library),
                'file_path': str(file_path),
                'title': title,
                'artist': artist,
                'album': album,
                'image': image
            }
        )
        log.info(f'{artist} - {title} updated')
    else:
        db.insert_document(
            music_collection,
            {
                'library': str(library),
                'file_path': str(file_path),
                'title': title,
                'artist': artist,
                'album': album,
                'image': image
            }
        )
        log.info(f'{artist} - {title} added to {library}')


if __name__ == '__main__':
    # load_data_to_db(TARGET_DIR, TARGET_DIR)
    find_duplicates()
