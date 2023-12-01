import os
import webbrowser

from pathlib import Path
from tkinter import *
from tkinter import messagebox, filedialog

from utils.logger import log
from utils.tag_changer import tag_change, delete_images
from db.db_controller import (load_data_to_db, find_duplicates, to_delete, clean_library, synchronization_with_main,
                              to_sync)


CURRENT_DIR = Path(os.path.realpath(__file__)).parent
README_FILE = Path(CURRENT_DIR, '../README.md')
SETTINGS_FILE = Path(CURRENT_DIR, '../settings.txt')
SETTINGS_KEYS = ['SOURCE_DIR', 'ARTIST_DIRS', 'SYNC_DIRS']


def show_message(window: Tk, title: str = None, message: str = None, error: Exception = None) -> None:
    if error:
        messagebox.showerror('Что-то пошло не так =(', str(error))
        log.error(error)
        window.destroy()
    else:
        messagebox.showinfo(title, message)


def chose_dir(dir_value: StringVar) -> None:
    star_value = dir_value.get()
    new_value = filedialog.askdirectory()
    if new_value:
        dir_value.set(new_value)
    else:
        dir_value.set(star_value)

    log.info(f'Was chosen directory: {dir_value.get()}')


def open_readme_file() -> None:
    webbrowser.open(str(README_FILE))
    log.info('Opening readme file')


def save_settings(window: Tk, **kwargs) -> None:
    settings = parse_settings(window)
    for key in settings:
        if key.lower() in kwargs:
            value = kwargs[key.lower()].get()
            settings[key] = value if value != '...' else ''
        if type(settings[key]) == list or type(settings[key]) == tuple:
            settings[key] = ', '.join(settings[key])

    with open(file=SETTINGS_FILE, mode='w') as file:
        for key, value in settings.items():
            file.write(f'{key}={value}\n')

    log.info(f'Settings have been saved: {settings=}')


def reset_settings() -> dict:
    settings = {}
    with open(file=SETTINGS_FILE, mode='w') as file:
        for key in SETTINGS_KEYS:
            file.write(f'{key}=\n')
            settings[key] = ''

    log.info('Settings have been reset')
    return settings


def update_values(settings: dict, **kwargs) -> None:
    for key, value in kwargs.items():
        key = key.upper()
        if key in ['ARTIST_DIRS', 'SYNC_DIR']:
            value.set(', '.join(settings[key]) if settings[key] else '...')
        else:
            value.set(settings[key] if settings[key] else '...')
    log.info('Values have been updated')


def parse_settings(window: Tk) -> dict:
    settings = {}
    try:
        with open(file=SETTINGS_FILE, mode='r') as file:
            for line in file:
                try:
                    key, value = line.split('=')
                    settings[key] = value.strip()
                except ValueError:
                    settings = raise_file_settings_error(window)
                    break
    except FileNotFoundError:
        settings = reset_settings()

    if settings is None:
        return {}

    for key in SETTINGS_KEYS:
        if key not in settings:
            raise_file_settings_error(window)
            break
        else:
            if key in ['ARTIST_DIRS', 'SYNC_DIRS']:
                try:
                    if settings[key]:
                        settings[key] = list(map(lambda x: x.strip(), settings[key].split(',')))
                except ValueError:
                    settings = raise_file_settings_error(window)
                    break

    log.info(f'Finish parsing settings: {settings=}')
    return settings


def press_reset_button(**kwargs) -> None:
    settings = reset_settings()
    update_values(settings, **kwargs)


def start_tag_changer(target_dir: StringVar, artist_dirs: StringVar, is_main: BooleanVar, window: Tk) -> None:
    log.info('tag_changer start')
    target_dir = Path(target_dir.get())
    artist_dirs = artist_dirs.get().split(',')
    try:
        tag_change(target_dir, target_dir, artist_dirs)
        if is_main.get():
            clean_library('Main')
            load_data_to_db(target_dir, target_dir, True)
            log.info(f'Datas load to Main.')
        delete_images(target_dir)
        show_message(window, 'Tag Changer завершил работу', 'Файлы были изменены.')
    except Exception as e:
        show_message(window, error=e)
    log.info('tag_changer finish')


def start_duplicate_finding(window: Tk, duplicates: Variable) -> None:
    log.info('duplicate_finding start')
    try:
        data = find_duplicates()
        if data:
            duplicates.set(data)
        else:
            duplicates.set(['Дубликатов не найдено'])
        show_message(window, message='Писк дубликатов завершён.')
    except Exception as e:
        show_message(window, error=e)


def raise_file_settings_error(window: Tk) -> dict | None:
    log.info(f'Start settings file error')
    messagebox.showerror(
        'Ошибка',
        'Ваш файл настроек повреждён. Пожалуйста, исправьте файл или сбросьте настройки.'
    )
    answer = messagebox.askyesno(
        'Сброс настроек',
        'Установить настройки по умолчанию?\n (в случае отказа программа прекратит работу)'
    )

    if answer:
        settings = reset_settings()
    else:
        log.error('Wrong settings file.')
        window.destroy()
        settings = None

    log.info(f'End settings file error')
    return settings


def delete_duplicates(window: Tk, results: Listbox) -> None:
    duplicates = [results.get(i).strip() for i in results.curselection()]
    try:
        for d in duplicates:
            to_delete('Main', d)
        results.delete(0, END)
        results.insert(0, 'Запустите поиск ещё раз, если хотите проверить,',
                       'или синхронизируйте вашу основную библиотеку с остальными.')
        show_message(window, message='Дубликаты были успешно удалены.')
    except Exception as e:
        show_message(window, error=e)


def add_dir_to_list(sync_list: Variable, dir_to_add: StringVar):
    dir_to_add = dir_to_add.get()
    log.info(f'add dir "{dir_to_add}" to sync list')
    data = sync_list.get()
    if data == ('...',):
        data = []
    data = list(set([*data] + [dir_to_add]))
    sync_list.set(data)


def chose_all_in_list(sync_list: Listbox, variable: BooleanVar):
    size = sync_list.size()
    if not variable.get():
        sync_list.select_set(0, size)
    else:
        sync_list.select_clear(0, size)


def sync_search(results: Listbox) -> [list[str], list[str]]:
    clean_library({'$ne': 'Main'})
    directories = [results.get(i) for i in results.curselection()]
    for directory in directories:
        load_data_to_db(Path(directory), Path(directory), False)
    data = synchronization_with_main(*directories)

    return data, directories


def delete_sync(results: Listbox):
    results = [results.get(i).strip().split(' --> ') for i in results.curselection()]
    for library, element in results:
        to_delete(library, element)


def add_sync(results: Listbox, libraries: list[str]):
    results = [results.get(i).strip().split(' --> ') for i in results.curselection()]
    for library, element in results:
        if library == 'Main':
            log.warning(f"Can't find object ({library}/{element}) that exist only in db.")
            continue
        libs = list(filter(lambda x: x != library, libraries))
        to_sync(library, element, libs)
