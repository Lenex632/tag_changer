from tkinter import *
from tkinter import ttk

from tkinter import messagebox, Checkbutton

from logger import log
from db_controller import synchronization_with_main, load_data_to_db, find_duplicates


def make_window() -> Tk:
    window = Tk()
    window.title("Поиск дубликатов")
    window.resizable(False, False)

    w = 600
    h = 300
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    window.geometry(f'{w}x{h}+{x}+{y}')

    log.info(f'Making window name="{window.title()}".')
    return window


def make_buttons_frame() -> Button:
    buttons_frame = ttk.Frame(padding=[8, 10])

    start_button = Button(buttons_frame, text='Запустить поиск   >>')
    start_button.pack(side=LEFT)

    buttons_frame.pack(anchor=NW, fill=X, pady=10, padx=10)

    log.info('Making frame for buttons.')
    return start_button


def end_duplicate_finding(window: Tk, error: Exception = None) -> None:
    if error:
        messagebox.showerror('Что-то пошло не так =(', str(error))
        log.error(error)
        window.destroy()
    messagebox.showinfo(
        'Писк дубликатов завершил работу',
        'Файлы были изменены. Нажмите "ОК", чтобы выйти'
    )
    log.info(f'duplicate_finding finish')
    window.destroy()


def start_duplicate_finding(window: Tk) -> None:
    log.info('duplicate_finding start')
    try:
        find_duplicates()
    except Exception as e:
        end_duplicate_finding(window, e)
    print('\n')
    end_duplicate_finding(window)


def main():
    data = find_duplicates()

    window = make_window()

    start_btn = make_buttons_frame()
    start_btn.bind('<ButtonPress-1>', lambda x: start_duplicate_finding(window))

    results_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])

    label = Label(results_frame, text=f'Результаты поиска:')
    label.grid(row=0, column=0, sticky=W, columnspan=2)
    count = 1
    row = 2
    for artist, title, file_path in data:
        artist_title = Label(results_frame, justify=LEFT, text=f'{count}) {artist} - {title}')
        artist_title.grid(row=row, column=0, sticky=W, columnspan=2)
        row += 1
        count += 1
        for path in file_path:
            checkbox = Checkbutton(results_frame)
            checkbox.grid(row=row, column=0, sticky=N)
            element = Label(results_frame, justify=LEFT, text=f'{path}')
            element.grid(row=row, column=1, sticky=W)
            row += 1

    results_frame.pack(anchor=NW, fill=X, padx=10, pady=10)

    log.info(f'Making frame for {results_frame}.')

    window.mainloop()


if __name__ == '__main__':
    main()
