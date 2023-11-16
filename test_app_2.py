from tkinter import *
from tkinter import ttk

from tkinter import messagebox

from logger import log
from db_controller import synchronization_with_main, load_data_to_db, find_duplicates, ask_to_delete


def make_window() -> Tk:
    window = Tk()
    window.title("Поиск дубликатов")
    window.resizable(False, False)

    w = 600
    h = 400
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    window.geometry(f'{w}x{h}+{x}+{y}')

    log.info(f'Making window name="{window.title()}".')
    return window


def show_message(window: Tk, text: str = None, error: Exception = None) -> None:
    if error:
        messagebox.showerror('Что-то пошло не так =(', str(error))
        log.error(error)
        window.destroy()
    else:
        messagebox.showinfo(message=text)


def start_duplicate_finding(window: Tk, duplicates: Variable) -> None:
    log.info('duplicate_finding start')
    try:
        data = find_duplicates()
        if data:
            duplicates.set(data)
        else:
            duplicates.set(['Дубликатов не найдено'])
        show_message(window, 'Писк дубликатов завершён.')
    except Exception as e:
        show_message(window, error=e)


def delete_duplicates(window: Tk, results: Listbox) -> None:
    duplicates = [results.get(i) for i in results.curselection()]
    try:
        ask_to_delete('Main', duplicates)
        results.delete(0, END)
        results.insert(0, 'Запустите поиск ещё раз, что бы продолжить.')
        show_message(window, 'Дубликаты были успешно удалены.')
    except Exception as e:
        show_message(window, error=e)


def main():
    window = make_window()

    duplicates = Variable(value=['Запустите поиск, что бы продолжить.'])

    start_btn = Button(text='Запустить поиск   >>')
    start_btn.pack(anchor=NW, pady=10, padx=10)
    start_btn.bind('<ButtonPress-1>', lambda x: start_duplicate_finding(window, duplicates))

    label = Label(text=f'Результаты поиска:')
    label.pack(anchor=NW, padx=10)

    results_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10], height=1000)
    results_frame.pack(anchor=NW, fill=X, padx=10, pady=10)

    results = Listbox(results_frame, listvariable=duplicates, selectmode=MULTIPLE)
    results.pack(anchor=NW, fill=X, side=LEFT, expand=1)
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results.yview)
    scrollbar.pack(anchor=NW, fill=Y, side=RIGHT)
    results["yscrollcommand"] = scrollbar.set

    label = Label(text=f'Выделите файлы, которые хотите удалить и нажмите кнопку "Удалить".')
    label.pack(anchor=NW, padx=10)

    delete_btn = Button(text='Удалить')
    delete_btn.pack(anchor=NW, side=RIGHT, pady=10, padx=10)
    delete_btn.bind('<ButtonPress-1>', lambda x: delete_duplicates(window, results))

    log.info(f'Making frame for {results_frame}.')

    window.mainloop()


if __name__ == '__main__':
    main()
