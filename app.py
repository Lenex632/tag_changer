import os
import webbrowser

from pathlib import Path
from tkinter import *
from tkinter import ttk

from tkinter import messagebox
from tkinter import filedialog

from tag_changer import tag_change, delete_images

CURRENT_DIR = Path(os.path.realpath(__file__)).parent
SETTINGS_FILE = Path(CURRENT_DIR, 'settings.txt')
SETTINGS_KEYS = ['SOURCE_DIR', 'ARTIST_DIRS']
README_FILE = Path(CURRENT_DIR, 'README.md')


def make_window() -> Tk:
    window = Tk()
    window.title("Tag Changer")
    window.resizable(False, False)

    w = 600
    h = 300
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    window.geometry(f'{w}x{h}+{x}+{y}')

    print(f'Making window name="{window.title()}".')
    return window


def make_dir_frame(target: str) -> tuple[Frame, StringVar]:
    match target:
        case 'source_dir':
            text = 'Укажите путь к исходной папке'
        case 'artist_dirs':
            text = 'Укажите папки с исполнителями для Уровня 2 (через запятую)'
        case _:
            text = ''

    frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])

    label = Label(frame, text=f'{text}')
    label.pack(anchor=NW)

    value = StringVar(value='...')
    if target == 'source_dir':
        btn = Button(frame, text='O', command=lambda v=value: chose_dir(v))
        btn.pack(side=LEFT, pady=3)

    entry = Entry(frame, textvariable=value)
    entry.pack(fill=X, padx=5, pady=3, ipady=4)

    frame.pack(anchor=NW, fill=X, padx=10, pady=10)

    print(f'Making frame for {target}.')
    return frame, value


def make_buttons_frame() -> tuple[Frame, Button, Button, Button]:
    buttons_frame = ttk.Frame(padding=[8, 10])

    readme_button = Button(buttons_frame, text='Открыть ReadMe', command=open_readme_file)
    readme_button.pack(anchor=NW)

    reset_button = Button(buttons_frame, text='Сбросить настройки')
    reset_button.pack(side=LEFT)

    start_button = Button(buttons_frame, text='Запуск   >>')
    start_button.pack(side=RIGHT)

    save_button = Button(buttons_frame, text='Сохранить настройки')
    save_button.pack(side=RIGHT)

    buttons_frame.pack(anchor=NW, fill=X, pady=10, padx=10)

    print('Making frame for buttons.')
    return buttons_frame, reset_button, start_button, save_button


def chose_dir(dir_value: StringVar) -> None:
    star_value = dir_value.get()
    new_value = filedialog.askdirectory()
    if new_value:
        dir_value.set(new_value)
    else:
        dir_value.set(star_value)

    print(f'Was chosen directory: {dir_value.get()}')


def save_settings(sd_value: StringVar, ad_value: StringVar) -> None:
    sd_value = sd_value.get() if sd_value.get() != '...' else ''
    ad_value = ad_value.get() if ad_value.get() != '...' else ''
    settings = dict(zip(SETTINGS_KEYS, (sd_value, ad_value)))

    with open(file=SETTINGS_FILE, mode='w') as file:
        for key, value in settings.items():
            file.write(f'{key}={value}\n')

    print('Settings have been saved')


def reset_settings() -> dict:
    settings = {}
    with open(file=SETTINGS_FILE, mode='w') as file:
        for key in SETTINGS_KEYS:
            file.write(f'{key}=\n')
            settings[key] = ''

    print('Settings have been reset')
    return settings


def update_values(settings: dict, **kwargs) -> None:
    kwargs['sd_value'].set(settings['SOURCE_DIR'] if settings['SOURCE_DIR'] else '...')
    kwargs['ad_value'].set(', '.join(settings['ARTIST_DIRS']) if settings['ARTIST_DIRS'] else '...')
    print('Values have been updated')


def press_reset_button(**kwargs) -> None:
    settings = reset_settings()
    update_values(settings, **kwargs)


def open_readme_file() -> None:
    webbrowser.open(str(README_FILE))
    print('Opening readme file')


def start_tag_changer(target_dir: StringVar, artist_dirs: StringVar) -> None:
    print('tag_changer start')
    target_dir = Path(target_dir.get())
    artist_dirs = artist_dirs.get().split(',')  # TODO потестить "Легенды"
    tag_change(target_dir, target_dir, artist_dirs)
    print('\n')
    delete_images(target_dir)


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

    print(f'Finish parsing settings: {settings=}')
    return settings


def raise_file_settings_error(window: Tk) -> dict | None:
    print(f'Start settings file error')
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
        window.destroy()
        settings = None

    print(f'End settings file error')
    return settings


def main():
    window = make_window()
    sd_frame, sd_value = make_dir_frame('source_dir')
    ad_frame, ad_value = make_dir_frame('artist_dirs')
    btn_frame, reset_btn, start_btn, save_btn = make_buttons_frame()

    save_btn.bind('<ButtonPress-1>', lambda x: save_settings(sd_value, ad_value))
    reset_btn.bind('<ButtonPress-1>', lambda x: press_reset_button(sd_value=sd_value, ad_value=ad_value))
    start_btn.bind('<ButtonPress-1>', lambda x: start_tag_changer(sd_value, ad_value))

    settings = parse_settings(window)
    if settings:
        update_values(settings, sd_value=sd_value, ad_value=ad_value)

    window.mainloop()


if __name__ == '__main__':
    main()
