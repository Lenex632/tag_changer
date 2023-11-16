import os
import webbrowser

from pathlib import Path
from tkinter import *
from tkinter import ttk

from tkinter import messagebox
from tkinter import filedialog

from tag_changer import tag_change, delete_images
from db_controller import synchronization_with_main, load_data_to_db, find_duplicates, ask_to_delete
from logger import log

CURRENT_DIR = Path(os.path.realpath(__file__)).parent
SETTINGS_FILE = Path(CURRENT_DIR, 'settings.txt')
SETTINGS_KEYS = ['SOURCE_DIR', 'ARTIST_DIRS']
README_FILE = Path(CURRENT_DIR, 'README.md')


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
        case _:
            text = ''

    frame = ttk.Frame(notebook, borderwidth=1, relief=SOLID, padding=[8, 10])

    label = Label(frame, text=f'{text}')
    label.pack(anchor=NW)

    value = StringVar(value='...')
    if target == 'source_dir':
        btn = Button(frame, text='O', command=lambda v=value: chose_dir(v))
        btn.pack(side=LEFT, pady=3)

    entry = Entry(frame, textvariable=value)
    entry.pack(fill=X, padx=5, pady=3, ipady=4)

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


def chose_dir(dir_value: StringVar) -> None:
    star_value = dir_value.get()
    new_value = filedialog.askdirectory()
    if new_value:
        dir_value.set(new_value)
    else:
        dir_value.set(star_value)

    log.info(f'Was chosen directory: {dir_value.get()}')


def save_settings(sd_value: StringVar, ad_value: StringVar) -> None:
    sd_value = sd_value.get() if sd_value.get() != '...' else ''
    ad_value = ad_value.get() if ad_value.get() != '...' else ''
    settings = dict(zip(SETTINGS_KEYS, (sd_value, ad_value)))

    with open(file=SETTINGS_FILE, mode='w') as file:
        for key, value in settings.items():
            file.write(f'{key}={value}\n')

    log.info('Settings have been saved')


def reset_settings() -> dict:
    settings = {}
    with open(file=SETTINGS_FILE, mode='w') as file:
        for key in SETTINGS_KEYS:
            file.write(f'{key}=\n')
            settings[key] = ''

    log.info('Settings have been reset')
    return settings


def update_values(settings: dict, **kwargs) -> None:
    kwargs['sd_value'].set(settings['SOURCE_DIR'] if settings['SOURCE_DIR'] else '...')
    kwargs['ad_value'].set(', '.join(settings['ARTIST_DIRS']) if settings['ARTIST_DIRS'] else '...')
    log.info('Values have been updated')


def press_reset_button(**kwargs) -> None:
    settings = reset_settings()
    update_values(settings, **kwargs)


def open_readme_file() -> None:
    webbrowser.open(str(README_FILE))
    log.info('Opening readme file')


def show_message(window: Tk, title: str = None, message: str = None, error: Exception = None) -> None:
    if error:
        messagebox.showerror('Что-то пошло не так =(', str(error))
        log.error(error)
        window.destroy()
    else:
        messagebox.showinfo(title, message)


def start_tag_changer(target_dir: StringVar, artist_dirs: StringVar, window: Tk) -> None:
    log.info('tag_changer start')
    target_dir = Path(target_dir.get())
    artist_dirs = artist_dirs.get().split(',')
    try:
        tag_change(target_dir, target_dir, artist_dirs)
    except Exception as e:
        show_message(window, error=e)
    print('\n')
    delete_images(target_dir)
    show_message(window, 'Tag Changer завершил работу', 'Файлы были изменены.')
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


def parse_settings(window: Tk) -> dict | None:
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
        return None

    for key in SETTINGS_KEYS:
        if key not in settings:
            raise_file_settings_error(window)
            break
        else:
            if key == 'ARTIST_DIRS':
                try:
                    if settings[key]:
                        settings[key] = list(map(lambda x: x.strip(), settings[key].split(',')))
                except ValueError:
                    settings = raise_file_settings_error(window)
                    break

    log.info(f'Finish parsing settings: {settings=}')
    return settings


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
    duplicates = [results.get(i) for i in results.curselection()]
    try:
        ask_to_delete('Main', duplicates)
        results.delete(0, END)
        results.insert(0, 'Запустите поиск ещё раз, если хотите проверить,',
                       'или синхронизируйте вашу основную библиотеку с остальными.')
        show_message(window, message='Дубликаты были успешно удалены.')
    except Exception as e:
        show_message(window, error=e)


def make_tag_changer_note(window: Tk, notebook: ttk.Notebook):
    tag_changer_manager = ttk.Frame(notebook)

    sd_value = make_dir_frame('source_dir', tag_changer_manager)
    ad_value = make_dir_frame('artist_dirs', tag_changer_manager)
    reset_btn, start_btn, save_btn = make_buttons_frame(tag_changer_manager)

    save_btn.bind('<ButtonPress-1>', lambda x: save_settings(sd_value, ad_value))
    reset_btn.bind('<ButtonPress-1>', lambda x: press_reset_button(sd_value=sd_value, ad_value=ad_value))
    start_btn.bind('<ButtonPress-1>', lambda x: start_tag_changer(sd_value, ad_value, window))

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
    synchronization_manager.pack(fill=BOTH, expand=True)
    notebook.add(synchronization_manager, text="Синхронизация")


def main():
    window, notebook = make_window()

    make_tag_changer_note(window, notebook)
    make_duplicate_note(window, notebook)
    make_synchronization_note(window, notebook)

    window.mainloop()


if __name__ == '__main__':
    main()
