from tkinter import *
from tkinter import ttk

from utils.logger import log
from app.app_functions import (chose_dir, open_readme_file, save_settings, press_reset_button, start_tag_changer,
                               parse_settings, update_values, start_duplicate_finding, delete_duplicates,
                               add_dir_to_list, sync_search, chose_all_in_list, delete_sync, add_sync)


def make_window() -> [Tk, ttk.Notebook]:
    window = Tk()
    window.title("Tag Changer")
    window.resizable(False, False)

    w = 600
    h = 400
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    window.geometry(f'{w}x{h}+{x}+{y}')

    notebook = ttk.Notebook(window)
    notebook.pack(expand=True, fill=BOTH)

    log.info(f'Making window name="{window.title()}".')
    return window, notebook


def make_dir_frame(target: str, frame: Frame) -> StringVar | tuple[StringVar, Button]:
    match target:
        case 'source_dir':
            text = 'Укажите путь к исходной папке'
        case 'artist_dirs':
            text = 'Укажите папки с исполнителями для Уровня 2 (через запятую)'
        case 'sync_dirs':
            text = 'Укажите папку для синхронизации'
        case _:
            text = ''

    dir_frame = ttk.Frame(frame, borderwidth=1, relief=SOLID, padding=[8, 10])
    dir_frame.pack(anchor=NW, fill=X, padx=10, pady=10)

    label = Label(dir_frame, text=f'{text}')
    label.pack(anchor=NW)

    value = StringVar(value='...')
    if target in ['source_dir', 'sync_dirs']:
        btn = Button(dir_frame, text='O', command=lambda v=value: chose_dir(v))
        btn.pack(side=LEFT, pady=3)

    entry = Entry(dir_frame, textvariable=value)
    entry.pack(side=LEFT, fill=X, expand=1, padx=5, pady=3, ipady=4)

    if target == 'sync_dirs':
        add_dir_btn = Button(dir_frame, text='Добавить')
        add_dir_btn.pack(side=RIGHT)
        return value, add_dir_btn
    return value


def make_buttons_frame(frame: Frame) -> tuple[Button, Button, Button]:
    buttons_frame = ttk.Frame(frame, padding=[8, 10])
    buttons_frame.pack(anchor=NW, side=BOTTOM, fill=X)

    readme_button = Button(buttons_frame, text='Открыть ReadMe', command=open_readme_file)
    readme_button.pack(anchor=NW)

    reset_button = Button(buttons_frame, text='Сбросить настройки')
    reset_button.pack(side=LEFT)

    start_button = Button(buttons_frame, text='Запуск   >>')
    start_button.pack(side=RIGHT)

    save_button = Button(buttons_frame, text='Сохранить настройки')
    save_button.pack(side=RIGHT)

    return reset_button, start_button, save_button


def make_checkbox(text: str, frame: Frame) -> [BooleanVar, Checkbutton]:
    variable = BooleanVar()
    checkbox_btn = ttk.Checkbutton(frame, text=text, variable=variable)
    checkbox_btn.pack(anchor=NW, padx=10)

    return variable, checkbox_btn


def make_results(frame: ttk.Frame, variable: Variable) -> Listbox:
    results_frame = ttk.Frame(frame, borderwidth=1, relief=SOLID, padding=[8, 10])
    results_frame.pack(anchor=NW, fill=X, padx=10, pady=10)

    results = Listbox(results_frame, listvariable=variable, selectmode=MULTIPLE)
    results.pack(anchor=NW, fill=X, side=LEFT, expand=1)
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results.yview)
    scrollbar.pack(anchor=NW, fill=Y, side=RIGHT)
    results["yscrollcommand"] = scrollbar.set

    return results


def make_tag_changer_note(window: Tk, notebook: ttk.Notebook) -> None:
    tag_changer_manager = ttk.Frame(notebook)
    tag_changer_manager.pack(fill=BOTH, expand=True)
    notebook.add(tag_changer_manager, text="Изменить теги")

    source_dir = make_dir_frame('source_dir', tag_changer_manager)
    artist_dirs = make_dir_frame('artist_dirs', tag_changer_manager)
    is_main, is_main_btn = make_checkbox('Записать/Перезаписать как Main библиотеку', tag_changer_manager)
    reset_btn, start_btn, save_btn = make_buttons_frame(tag_changer_manager)

    settings = parse_settings(window)
    if settings:
        update_values(settings, source_dir=source_dir, artist_dirs=artist_dirs)

    save_btn.bind('<ButtonPress-1>', lambda x: save_settings(window, source_dir=source_dir, artist_dirs=artist_dirs))
    reset_btn.bind('<ButtonPress-1>', lambda x: press_reset_button(source_dir=source_dir, artist_dirs=artist_dirs))
    start_btn.bind('<ButtonPress-1>', lambda x: start_tag_changer(source_dir, artist_dirs, is_main, window))


def make_duplicate_note(window: Tk, notebook: ttk.Notebook) -> None:
    duplicate_manager = ttk.Frame(notebook)
    duplicate_manager.pack(fill=BOTH, expand=True)
    notebook.add(duplicate_manager, text="Найти дубликаты")
    duplicates = Variable(value=['Запустите поиск, что бы продолжить.'])

    start_btn = Button(duplicate_manager, text='Запустить поиск   >>')
    start_btn.pack(anchor=NW, pady=10, padx=10)
    start_btn.bind('<ButtonPress-1>', lambda x: start_duplicate_finding(window, duplicates))

    label = Label(duplicate_manager, text=f'Результаты поиска:')
    label.pack(anchor=NW, padx=10)

    results = make_results(duplicate_manager, duplicates)

    label = Label(duplicate_manager, text=f'Выделите файлы, которые хотите удалить и нажмите кнопку "Удалить".')
    label.pack(anchor=NW, padx=10)

    delete_btn = Button(duplicate_manager, text='Удалить')
    delete_btn.pack(anchor=NW, side=RIGHT, pady=10, padx=10)
    delete_btn.bind('<ButtonPress-1>', lambda x: delete_duplicates(window, results))


def make_synchronization_note(window: Tk, notebook: ttk.Notebook) -> None:
    synchronization_manager = ttk.Frame(notebook)
    synchronization_manager.pack(fill=BOTH, expand=True)
    notebook.add(synchronization_manager, text="Синхронизация")

    dir_to_add, add_btn = make_dir_frame('sync_dirs', synchronization_manager)
    reset_btn, start_btn, save_btn = make_buttons_frame(synchronization_manager)

    sync_dirs = Variable()
    chose_all, chose_all_btn = make_checkbox('Выбрать все', synchronization_manager)
    results = make_results(synchronization_manager, sync_dirs)

    settings = parse_settings(window)
    if settings:
        update_values(settings, sync_dirs=sync_dirs)

    chose_all_btn.bind('<ButtonPress-1>', lambda x: chose_all_in_list(results, chose_all))
    add_btn.bind('<ButtonPress-1>', lambda x: add_dir_to_list(sync_dirs, dir_to_add))
    save_btn.bind('<ButtonPress-1>', lambda x: save_settings(window, sync_dirs=sync_dirs))
    reset_btn.bind('<ButtonPress-1>', lambda x: press_reset_button(sync_dirs=sync_dirs))
    start_btn.bind('<ButtonPress-1>', lambda x: make_sync_window(sync_search(results)))


def make_sync_window(data: list[str]):
    sync_window = Toplevel()
    sync_window.resizable(False, False)
    sync_window.geometry('700x400')
    sync_window.title("Synchronization")

    sync_frame = ttk.Frame(sync_window)
    sync_frame.pack(fill=BOTH, expand=True, pady=10)

    label = Label(sync_frame, text=f'Результаты поиска:')
    label.pack(anchor=NW, padx=10)

    sync_data = Variable(value=data)
    results = make_results(sync_frame, sync_data)

    label = Label(sync_frame, text=f'Выделите файлы и нажмите кнопку "Удалить", чтобы удалить их с диска и/или из базы'
                                   f'\nданных, ИЛИ кнопку "Синхронизировать", чтобы добавить их в базу и/или в ваши '
                                   f'другие\nхранилища.', justify=LEFT)
    label.pack(anchor=NW, padx=10)

    delete_btn = Button(sync_frame, text='Удалить')
    delete_btn.pack(anchor=SW, side=RIGHT, padx=10)
    delete_btn.bind('<ButtonPress-1>', lambda x: delete_sync(results))
    delete_btn = Button(sync_frame, text='Синхронизировать')
    delete_btn.pack(anchor=SW, side=RIGHT)
    delete_btn.bind('<ButtonPress-1>', lambda x: add_sync(results))
