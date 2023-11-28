from app.app_construction import make_window, make_duplicate_note, make_tag_changer_note, make_synchronization_note


def main():
    window, notebook = make_window()

    make_tag_changer_note(window, notebook)
    make_duplicate_note(window, notebook)
    make_synchronization_note(window, notebook)

    window.mainloop()


if __name__ == '__main__':
    main()
