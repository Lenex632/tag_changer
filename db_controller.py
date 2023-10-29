from dataclasses import dataclass
from pathlib import Path
import eyed3

from logger import log
import db_functions as db
from tag_changer import SOURCE_DIR, TARGET_DIR


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
            load_data_to_db(core_dir, file, is_main_lib)
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
            except Exception as e:
                log.error(f'Error: {type(e)}. Can`t read parameter in file {file}.\n{str(e)}')
                continue

            _load_data_to_db(data)


def _load_data_to_db(data: MusicData) -> None:
    db.insert_document(main_lib, data.__dict__)
    log.info(f'{data.artist} - {data.title} added to {data.library}.')


def find_duplicates() -> list[tuple[str, str, list[str]]] | str | None:
    data = []
    duplicates = db.find_duplicates(main_lib)
    if not duplicates:
        log.info(f'There are no duplicates in Main library.')
        return 'Дубликатов нет'

    for duplicate in duplicates:
        artist, title = duplicate['name']
        elements = db.find_document(
            main_lib,
            {'$and': [{'title': title}, {'artist': artist}, {'library': 'Main'}]},
            {'file_path': 1, '_id': 0},
            multiple=True
        )
        file_path = [element['file_path'] for element in elements]
        data.append((artist, title, file_path))

    return data


def synchronization_with_main(*directories: str) -> None:
    unsync_file_path = db.find_different(main_lib, directories)

    if not unsync_file_path:
        print('Everything is synchronized')

    for file_path in unsync_file_path:
        data = db.find_document(main_lib, file_path, multiple=True)
        print(f'{data[0]["artist"]} - {data[0]["title"]}')
        for i in range(len(data)):
            print(i+1, data[i]['library'], '/', data[i]['file_path'])
        _ask_to_delete(data)
    # db.delete_document(
    #     main_lib,
    #     {'library': {'$ne': 'Main'}},
    #     multiple=True
    # )


def _ask_to_delete(elements: list) -> None:
    success = False
    while not success:
        elements_to_delete = input('\nEnter the numbers of elements you want to delete '
                                   '(in format 1 2 3) or 0 to cancel: ')

        try:
            elements_to_delete = list(map(int, elements_to_delete.split()))
        except ValueError:
            print(f'ValueError. You enter not numbers or not in write format')
            continue

        if 0 in elements_to_delete:
            log.info('Canceled\n')
            break

        for e in elements_to_delete:
            if e-1 not in range(len(elements)):
                log.warning(f'Index {e} out of range')
                break
        else:
            success = True
        if not success:
            continue

        for e in elements_to_delete:
            db.delete_document(main_lib, elements[e-1])
            # TODO удаление не сработает, если элемент в Main либе у которой нет реальных файлов, а только данные из БД.
            # Path(elements[e-1]['library'], elements[e-1]['file_path']).unlink()
            log.info(f'{elements[e-1]["file_path"]} was deleted from db')
        print()

        success = True


client, mydb, collections = db.db_connection()
main_lib = collections['main_lib_collection']


def main():
    # load_data_to_db(SOURCE_DIR, SOURCE_DIR, is_main_lib=True)
    # load_data_to_db(SOURCE_DIR, SOURCE_DIR, is_main_lib=False)
    # load_data_to_db(TARGET_DIR, TARGET_DIR, is_main_lib=False)
    data = find_duplicates()
    print(data)
    # synchronization_with_main(str(TARGET_DIR), str(SOURCE_DIR))
    # data = db.find_document(main_lib, {'library': 'Main'}, {'_id': 0}, multiple=True)
    # [print(d) for d in data]


if __name__ == '__main__':
    main()
    '''
    Хуярим логику:
    
        Хуярим структуру: !!!
            1) Юзер - чел с логином и паролем: !!!
                - у него есть одна базовая либа с его песнями +++
                - есть доп либы, которые добавляются и удаляются ---
                - что происходит при создании юзера ??? 
                  создать юзера = создать коллекцию юзер_мэйн_либа !!!
                  нужно ли создавать доп либы-коллекции или пхать всё в мэйн ---
            2) Либа - единое собрание всей музыки, что есть у юзера: +++
                - привязка к юзеру +++
                  либо создаваться в самом юзере и наполняться музыкой ---
                - есть имя (если это Main либа) или путь (если это доп либа) +++
                - есть путь ---
                - есть название ---
                - есть "основная либа" у каждого юзера которая называется "Main" +++
                - музыка с доп либ должна удаляться после завершения программы +++
            3) Музыка - описывает файлик с музыкой: +++
                - есть исполнитель - название - альбом +++
                - картинка +++
                - относительный путь (путь общий для всех дир на компе и на телефоне) +++
                - привязка к либе --- ??? либо создаётся в либе +++
                - если привязывать, то привязывать к id, имени или пути ??? ---
                - хранить в либе +++
                - всегда должны быть в Main либе +++
                                
        Функции: !!!
            1) Поиск +++
            2) Загрузка: +++
                - проходится по дире +++
                - для каждого файла заносить его в диру +++
            3) Удаление: +++
                - дубликатов +++
                - файлов что удалились в процессе синхронизации +++
            3) Поиск дубликатов: +++
                - внутренний поиск по Main силами бд +++
            4) Синхронизация: +++
                - сделать одну "основную либу" = Main +++
                - при запуске синхронизации сравнивать текущую папку с Main ---
                - выводить список различных файлов +++
                - сохранять отмеченные !!!
                - сделать тоже самое со второй папкой ---
                  сделать это одновременно, показать различия и
                устранить их сразу после чего сначала обновить Main, а потом дополнительные +++
    '''
