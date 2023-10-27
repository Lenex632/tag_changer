from dataclasses import dataclass
from pathlib import Path
import eyed3

from logger import log
import db_functions as db
from tag_changer import SOURCE_DIR, TARGET_DIR


client, mydb, collections = db.db_connection()
music_collection = collections['music_collection']
users_collection = collections['users_collection']
libraries_collection = collections['libraries_collection']


@dataclass
class MusicData:
    library: str = None
    file_path: str = None
    title: str = None
    artist: str = None
    album: str = None
    image: bool = None


def load_data_to_db(core_dir: Path, target_dir: Path, is_main_lib: bool = True) -> None:
    """
    Пробегаемся по directory, относительно core_directory, записываем файлы в БД с помощью _load_data_to_db()
    :param core_dir: неизменная директория относительно которой обрабатывается target_dir.
    :param target_dir: текущая директория, меняется соответственно уровню погружения.
    :param is_main_lib: флаг, указывает записывать ли в "основную" библиотеку или "вторичную".
    :return: None
    """
    for file in target_dir.iterdir():
        if file.is_dir():
            load_data_to_db(core_dir, file)
        elif file.is_file():
            data = MusicData()
            data.library = 'Main' if is_main_lib else str(core_dir)
            data.file_path = str(file.relative_to(core_dir))
            song = eyed3.load(file)
            try:
                data.title = song.tag.title
                data.artist = song.tag.artist
                data.album = song.tag.album
                if list(song.tag.images) and song.tag.images[0].image_data:
                    data.image = True
                else:
                    data.image = False
            except Exception as err:
                log.error(f'Error: {err.__class__.__name__}. Can`t read parameter in file {file}.')
                continue

            _load_data_to_db(data)


def _load_data_to_db(data: MusicData) -> None:
    db.insert_document(music_collection, data.__dict__)
    log.info(f'{data.artist} - {data.title} added to {data.library}')


# TODO разобраться с дубликатами из разных библиотек
def find_duplicates(library: str) -> None:
    duplicates = db.find_duplicates(music_collection, library)
    if not duplicates:
        log.info(f'There are no duplicates in {library}')

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
    # TODO Попробовать решить проблему синхронизации через поле валидности (уникальности)
    #       + Изначально при записи в БД - файл невалидный (мб уникальный). Тогда же проверяется, есть ли в БД такой же
    #  файл в другой библиотеке. Если есть - файл валидный, если нет - так и остаётся невалидным.
    #       + Вначале при изменении - находится такой же файл в другой библиотеке и становится невалидным. В конце
    #  изменения - изменяемый файл проходит процедуру валидацию, его "прошлый близнец" не проходит. "Близнец" может
    #  стать валидным, только если изменяемый файл остался таким же, или в последующем появился другой файл, способный
    #  стать его "близнецом".
    #       +- При синхронизации искать в двух библиотеках (мб перед этим обновить их валидность в обеих библиотеках)
    #  все невалидные файлы и решать, что с ними делать.
    #       Возникает проблема при локальном удалении файла. Валидность не обновляется. Решение: нужно добавлять время
    #  обновления файла и сравнивать удалилось что-то или нет. В конце обновления базы - искать файлы с самым старым
    #  временем и запрашивать удаление из базы.

    unsync_files = db.find_document(
        music_collection,
        {'synchronized': False, '$or': [{'library': dir1}, {'library': dir2}]},
        multiple=True
    )
    if not unsync_files:
        log.info('Everything is in sync')
    for i in range(len(unsync_files)):
        print(f"{i + 1}. {unsync_files[i]['library']}{unsync_files[i]['file_path']} ------ "
              f"{unsync_files[i]['artist']} - {unsync_files[i]['title']}")

    _ask_to_delete(unsync_files)


def _ask_to_delete(elements: list) -> None:
    success = False
    while not success:
        elements_to_delete = input('\nEnter the numbers of elements you want to delete (in format 1 2 3) or 0 to cancel: ')

        try:
            elements_to_delete = list(map(int, elements_to_delete.split()))
        except ValueError:
            log.warning(f'ValueError. You enter not numbers or not in write format')
            continue

        if 0 in elements_to_delete:
            log.info('Canceled\n')
            break

        for e in elements_to_delete:
            if e - 1 not in range(len(elements)):
                log.warning(f'Index {e} out of range')
                break
        else:
            success = True
        if not success:
            continue

        for e in elements_to_delete:
            db.delete_document(music_collection, elements[e - 1])
            Path(elements[e - 1]['library'], elements[e - 1]['file_path']).unlink()
            log.info(f'{elements[e - 1]["file_path"]} was deleted from db')
        print()

        success = True


if __name__ == '__main__':
    '''
    Хуярим логику:
    
        Хуярим структуру:
            1) Юзер - чел с логином и паролем:
                - у него есть одна базовая либа с его песнями
                - есть доп либы, которые добавляются и удаляются ???
            2) Либа - единое собрание всей музыки, что есть у юзера:
                - привязка к юзеру ??? либо создаваться в самом юзере и наполняться музыкой
                - есть имя
                - есть путь
                - есть название
                - есть "основная либа" у каждого юзера которая называется "Main" 
            3) Музыка - описывает файлик с музыкой:
                - есть исполнитель - название - альбом
                - картинка
                - относительный путь (путь общий для всех дир на компе и на телефоне)
                - привязка к либе ??? либо создаётся в либе 
                - если привязывать, то привязывать к id, имени или пути ???
                                
        Функции:
            1) Поиск
            2) Загрузка:
                - проходится по дире
                - для каждого файла заносить его в диру
            3) Удаление
            3) Поиск дубликатов:
                - внутренний поиск по Main силами бд !!!
            4) Синхронизация: ???
                - сделать одну "основную либу" = Main
                - при запуске синхронизации сравнивать текущую папку с Main
                - выводить список различных файлов
                - удалять отмеченные
                - сделать тоже самое со второй папкой ??? сделать это одновременно, показать различия и
                устранить их сразу после чего сначала обновить Main, а потом дополнительные !!!
    '''
    md = MusicData('lib', 'path', 'title', 'artist', 'album', False)
    print(md.__dict__)

