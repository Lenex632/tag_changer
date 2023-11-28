from tkinter import *
from tkinter import ttk

from utils.logger import log
from app.app_functions import (chose_dir, open_readme_file, save_settings, press_reset_button, start_tag_changer,
                               parse_settings, update_values, start_duplicate_finding, delete_duplicates)


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


def make_dir_frame(target: str, notebook: Frame) -> StringVar:
    match target:
        case 'source_dir':
            text = 'Укажите путь к исходной папке'
        case 'artist_dirs':
            text = 'Укажите папки с исполнителями для Уровня 2 (через запятую)'
        case 'sync_dir':
            text = 'Укажите папку для синхронизации'
        case _:
            text = ''

    frame = ttk.Frame(notebook, borderwidth=1, relief=SOLID, padding=[8, 10])

    label = Label(frame, text=f'{text}')
    label.pack(anchor=NW)

    value = StringVar(value='...')
    if target in ['source_dir', 'sync_dir']:
        btn = Button(frame, text='O', command=lambda v=value: chose_dir(v))
        btn.pack(side=LEFT, pady=3)

    entry = Entry(frame, textvariable=value)
    entry.pack(side=LEFT, fill=X, expand=1, padx=5, pady=3, ipady=4)

    if target == 'sync_dir':
        add_dir_btn = Button(frame, text='Добавить')
        add_dir_btn.pack(side=RIGHT, pady=10)

    frame.pack(anchor=NW, fill=X, padx=10, pady=10)

    return value


def make_buttons_frame(notebook: Frame) -> tuple[Button, Button, Button]:
    buttons_frame = ttk.Frame(notebook, padding=[8, 10])

    readme_button = Button(buttons_frame, text='Открыть ReadMe', command=open_readme_file)
    readme_button.pack(anchor=NW)

    reset_button = Button(buttons_frame, text='Сбросить настройки')
    reset_button.pack(side=LEFT)

    start_button = Button(buttons_frame, text='Запуск   >>')
    start_button.pack(side=RIGHT)

    save_button = Button(buttons_frame, text='Сохранить настройки')
    save_button.pack(side=RIGHT)

    buttons_frame.pack(anchor=NW, side=BOTTOM, fill=X)

    return reset_button, start_button, save_button


def make_main_checkbox(text: str, notebook: Frame) -> BooleanVar:
    is_main = BooleanVar()
    main_checkbox = ttk.Checkbutton(notebook, text=text, variable=is_main)
    main_checkbox.pack(anchor=NW, padx=10)
    return is_main


def make_tag_changer_note(window: Tk, notebook: ttk.Notebook):
    tag_changer_manager = ttk.Frame(notebook)

    sd_value = make_dir_frame('source_dir', tag_changer_manager)
    ad_value = make_dir_frame('artist_dirs', tag_changer_manager)
    is_main = make_main_checkbox('Записать/Перезаписать как Main библиотеку', tag_changer_manager)
    reset_btn, start_btn, save_btn = make_buttons_frame(tag_changer_manager)

    save_btn.bind('<ButtonPress-1>', lambda x: save_settings(sd_value, ad_value))
    reset_btn.bind('<ButtonPress-1>', lambda x: press_reset_button(sd_value=sd_value, ad_value=ad_value))
    start_btn.bind('<ButtonPress-1>', lambda x: start_tag_changer(sd_value, ad_value, is_main, window))

    tag_changer_manager.pack(fill=BOTH, expand=True)
    notebook.add(tag_changer_manager, text="Изменить теги")

    settings = parse_settings(window)
    if settings:
        update_values(settings, sd_value=sd_value, ad_value=ad_value)


def make_duplicate_note(window: Tk, notebook: ttk.Notebook):
    duplicate_manager = ttk.Frame(notebook)

    duplicates = Variable(value=['Запустите поиск, что бы продолжить.'])

    start_btn = Button(duplicate_manager, text='Запустить поиск   >>')
    start_btn.pack(anchor=NW, pady=10, padx=10)
    start_btn.bind('<ButtonPress-1>', lambda x: start_duplicate_finding(window, duplicates))

    label = Label(duplicate_manager, text=f'Результаты поиска:')
    label.pack(anchor=NW, padx=10)

    results_frame = ttk.Frame(duplicate_manager, borderwidth=1, relief=SOLID, padding=[8, 10], height=1000)
    results_frame.pack(anchor=NW, fill=X, padx=10, pady=10)

    results = Listbox(results_frame, listvariable=duplicates, selectmode=MULTIPLE)
    results.pack(anchor=NW, fill=X, side=LEFT, expand=1)
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results.yview)
    scrollbar.pack(anchor=NW, fill=Y, side=RIGHT)
    results["yscrollcommand"] = scrollbar.set

    label = Label(duplicate_manager, text=f'Выделите файлы, которые хотите удалить и нажмите кнопку "Удалить".')
    label.pack(anchor=NW, padx=10)

    delete_btn = Button(duplicate_manager, text='Удалить')
    delete_btn.pack(anchor=NW, side=RIGHT, pady=10, padx=10)
    delete_btn.bind('<ButtonPress-1>', lambda x: delete_duplicates(window, results))

    duplicate_manager.pack(fill=BOTH, expand=True)
    notebook.add(duplicate_manager, text="Найти дубликаты")


def make_synchronization_note(window: Tk, notebook: ttk.Notebook):
    synchronization_manager = ttk.Frame(notebook)

    label = Label(synchronization_manager, text=f'Перед синхронизацией внимательно прочитайте инструкцию.')
    label.pack(anchor=NW, padx=10)

    make_dir_frame('sync_dir', synchronization_manager)
    # add_dir_btn.bind('<ButtonPress-1>', lambda x: delete_duplicates(window, results))

    synchronization_manager.pack(fill=BOTH, expand=True)
    notebook.add(synchronization_manager, text="Синхронизация")
