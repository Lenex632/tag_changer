import eyed3
from pathlib import Path
from shutil import copy

import db.db_functions as db

from utils.logger import log
from utils.tag_changer import SOURCE_DIR, TARGET_DIR
from utils.model import MusicData


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


def find_duplicates() -> list[str]:
    data = []
    duplicates = db.find_duplicates(main_lib)
    if not duplicates:
        log.info(f'There are no duplicates in Main library.')
        return ['Дубликатов нет']

    for duplicate in duplicates:
        artist, title = duplicate['name']
        elements = db.find_document(
            main_lib,
            {'$and': [{'title': title}, {'artist': artist}, {'library': 'Main'}]},
            {'file_path': 1, '_id': 0},
            multiple=True
        )
        file_path = [element['file_path'] for element in elements]
        data.append(f'{artist} - {title}')
        for name in file_path:
            data.append(f'    {name}')

    return data


def synchronization_with_main(*directories: str) -> list[str]:
    unsync_file_path = db.find_different(main_lib, directories)
    datas = []

    if not unsync_file_path:
        return ['Всё синхронизировано. Пожалуйста закройте окно.']

    for file_path in unsync_file_path:
        data = db.find_document(main_lib, file_path, multiple=True)
        datas.append(f'{data[0]["artist"]} - {data[0]["title"]}')
        for i in range(len(data)):
            datas.append(f"    {data[i]['library']} --> {data[i]['file_path']}")
    return datas


def to_delete(library: str, element: str) -> None:
    db.delete_document(main_lib, {'$and': [{'file_path': element}, {'library': library}]})
    if library != 'Main':
        Path(library, element).unlink()
    log.info(f'{library}/{element} was deleted from db{" and from disk" if library != "Main" else ""}.')


def clean_library(library: str | dict) -> None:
    db.delete_document(main_lib, {'library': library}, multiple=True)


def to_sync(library: str, element: str, libs: list[str]) -> None:
    for lib in libs:
        copy(Path(library, element), Path(lib, element))
        data = MusicData(
            **db.find_document(
                main_lib,
                {'$and': [{'library': library}, {'file_path': element}]},
                {'_id': 0}
            )
        )
        data.library = 'Main'
        _load_data_to_db(data)
        log.info(f'{library}/{element} was coped to {lib}/{element}.')


client, mydb, collections = db.db_connection()
main_lib = collections['main_lib_collection']


def main():
    # db.delete_document(main_lib, {}, multiple=True)
    # load_data_to_db(SOURCE_DIR, SOURCE_DIR, is_main_lib=True)
    # load_data_to_db(SOURCE_DIR, SOURCE_DIR, is_main_lib=False)
    # load_data_to_db(TARGET_DIR, TARGET_DIR, is_main_lib=False)
    # datas = find_duplicates()
    # ask_to_delete('Main', datas)
    # data = synchronization_with_main(str(TARGET_DIR), str(SOURCE_DIR))
    # data = db.find_document(main_lib, {'library': 'Main'}, {'_id': 0}, multiple=True)
    # [print(d) for d in data]
    to_sync('/home/lenex/code/tag_changeer/target_dir',
            'The Best/Taio Cruz, Some Artis, Some2 - Dynamite (feat. Some1).mp3',
            ['/home/lenex/code/tag_changeer/source_dir'])


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
            4) Синхронизация: !!!
                - сделать одну "основную либу" = Main +++
                - при запуске синхронизации сравнивать текущую папку с Main ---
                - выводить список различных файлов +++
                - сохранять отмеченные !!!
                - сделать тоже самое со второй папкой ---
                  сделать это одновременно, показать различия и
                устранить их сразу после чего сначала обновить Main, а потом дополнительные +++
    '''
