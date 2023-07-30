from pathlib import Path
import eyed3

from logger import log
import db_functions as db
from tag_changer import SOURCE_DIR, TARGET_DIR


client, mydb, collections = db.db_connection()
music_collection = collections['music_collection']
users_collection = collections['users_collection']
libraries_collection = collections['libraries_collection']


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

            _load_data_to_db(core_directory.__str__(), file_relative_position.__str__(), title, artist, album, image)


def find_duplicates(library: str) -> None:
    duplicates = db.find_duplicates(music_collection, library)
    if not duplicates:
        print(f'There are no duplicates in {library}')

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

            _ask_to_delete(elements)


def synchronization(dir1: str, dir2: str) -> None:
    """
        Попробовать решить проблему синхронизации через поле валидности (уникальности)

         + Изначально при записи в БД - файл невалидный (мб уникальный). Тогда же проверяется, есть ли в БД такой же
        файл в другой библиотеке. Если есть - файл валидный, если нет - так и остаётся невалидным.

         + Вначале при изменении - находится такой же файл в другой библиотеке и становится невалидным. В конце
        изменения - изменяемый файл проходит процедуру валидацию, его "прошлый близнец" не проходит. "Близнец" может
        стать валидным, только если изменяемый файл остался таким же, или в последующем появился другой файл, способный
        стать его "близнецом".

         +- При синхронизации искать в двух библиотеках (мб перед этим обновить их валидность в обеих библиотеках) все
        невалидные файлы и решать, что с ними делать.

        Возникает проблема при локальном удалении файла. Валидность не обновляется. Решение: нужно добавлять время
        обновления файла и сравнивать удалилось что-то или нет. В конце обновления базы - искать файлы с самым старым
        временем и запрашивать удаление из базы.
    """
    # TODO
    unsync_files = db.find_document(
        music_collection,
        {'synchronized': False, '$or': [{'library': dir1}, {'library': dir2}]},
        multiple=True
    )
    for i in range(len(unsync_files)):
        print(f"{i + 1}. {unsync_files[i]['library']}{unsync_files[i]['file_path']} ------ "
              f"{unsync_files[i]['artist']} - {unsync_files[i]['title']}")

    _ask_to_delete(unsync_files)


def _load_data_to_db(library: str, file_path: str, title: str, artist: str, album: str, image: bool,
                     synchronized: bool = False) -> None:
    new_data = {
        'library': library,
        'file_path': file_path,
        'title': title,
        'artist': artist,
        'album': album,
        'image': image,
        'synchronized': synchronized,
        'updated_time': None
    }
    if db.find_document(music_collection, {'file_path': file_path, 'library': library}):
        new_data.pop('library')
        synch_data = db.find_document(music_collection, {'file_path': file_path}, multiple=True)
        if len(synch_data) > 1:
            for data in synch_data:
                if not data['synchronized']:
                    synchronized = True
                db.update_document(music_collection, data, {'synchronized': synchronized})

        new_data['library'] = library
        new_data['synchronized'] = synchronized
        db.update_document(music_collection, {'file_path': file_path, 'library': library}, new_data)
        log.info(f'{artist} - {title} updated')
    else:
        new_data.pop('library')
        synch_data = db.find_document(music_collection, new_data)
        if synch_data:
            synchronized = True
            db.update_document(music_collection, new_data, {'synchronized': synchronized})
            new_data['synchronized'] = synchronized

        new_data['library'] = library
        db.insert_document(music_collection, new_data)
        log.info(f'{artist} - {title} added to {library}')


def _ask_to_delete(elements: list) -> None:
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
            db.delete_document(music_collection, elements[e - 1])
            Path(elements[e - 1]['library'], elements[e - 1]['file_path']).unlink()
            print(f'{elements[e - 1]["file_path"]} was deleted from db')
        print()

        success = True


if __name__ == '__main__':
    # load_data_to_db(SOURCE_DIR, SOURCE_DIR)
    # load_data_to_db(TARGET_DIR, TARGET_DIR)
    # synchronization(TARGET_DIR.__str__(), SOURCE_DIR.__str__())
    # find_duplicates()
    log.info('some message1')
