from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter.ttk import Checkbutton
from tkinter.ttk import Progressbar


def clicked():
    res = txt.get()
    lbl.configure(text=f'Hi, {res}!')


def get_result():
    res = selected.get()
    result.configure(text=f'result = {res}')


def show_message():
    # messagebox.showinfo('Title', 'Text')
    # messagebox.showwarning('Title', 'Text')
    messagebox.showerror('Title', 'Text')


def chose_file():
    file = filedialog.askopenfilename()
    file_txt.configure(text=file)


def main_tabs():
    tabs = Tk()
    tabs.geometry('600x600')
    tabs.title("Tag Changer")

    tab_control = ttk.Notebook(tabs)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)

    tab_control.add(tab1, text='Первая')
    tab_control.add(tab2, text='Вторая')
    lbl1 = Label(tab1, text='Вкладка 1')
    lbl1.grid(column=0, row=0)
    lbl2 = Label(tab2, text='Вкладка 2')
    lbl2.grid(column=0, row=0)
    tab_control.pack(expand=1, fill='both')

    tabs.mainloop()


def main():
    window = Tk()
    window.geometry('600x600')
    window.title("Tag Changer")

    for c in range(3):
        window.columnconfigure(index=c, weight=1, pad=10)

    lbl = Label(window, text="Hellow world", font=("Arial Bold", 30))
    lbl.grid(column=0, row=0, columnspan=2)

    btn = Button(window, text="Dont touch!", bg='Red', command=clicked)
    btn.grid(column=0, row=1)

    txt = Entry(window, width=10)
    txt.grid(column=1, row=1)
    txt.focus()

    combo = Combobox(window, width=10)
    combo['values'] = (1, 2, 3, 4, 5, "Text")
    combo.current(1)  # установите вариант по умолчанию
    combo.grid(column=2, row=0)

    chk_state = BooleanVar()
    chk_state.set(True)  # задайте проверку состояния чекбокса
    chk = Checkbutton(window, text='Chose', variable=chk_state)
    chk.grid(column=0, row=2, padx=10, pady=10)

    selected = IntVar()
    rad1 = Radiobutton(window, text='First', value=1, variable=selected, command=get_result)
    rad2 = Radiobutton(window, text='Second', value=2, variable=selected, command=get_result)
    rad3 = Radiobutton(window, text='Third', value=3, variable=selected, command=get_result)
    rad1.grid(column=0, row=3)
    rad2.grid(column=1, row=3)
    rad3.grid(column=2, row=3)
    result = Label(window, text='result is None')
    result.grid(column=1, row=4)

    txt_f = scrolledtext.ScrolledText(window, height=10)
    txt_f.grid(column=0, row=5, columnspan=3, padx=10, pady=10)
    txt_f.insert(INSERT, 'Text field')

    msg_btn = Button(window, text='message in window', command=show_message)
    msg_btn.grid(column=0, row=6)

    spin = Spinbox(window, from_=-10, to=10, textvariable=IntVar(value=2))
    spin.grid(column=1, row=6)

    bar = Progressbar(window)
    bar.grid(column=2, row=7)
    bar['value'] = 40
    start_btn = Button(text="Start", command=lambda: bar.start(100))
    start_btn.grid(column=0, row=7)
    stop_btn = Button(text="Stop", command=lambda: bar.stop())
    stop_btn.grid(column=1, row=7)

    file_btn = Button(window, text='Chose file', command=chose_file)
    file_btn.grid(column=0, row=8, pady=10)
    file_txt = Label(window)
    file_txt.grid(column=1, row=8, columnspan=2)

    window.mainloop()


if __name__ == '__main__':
    main()
    # main_tabs()
