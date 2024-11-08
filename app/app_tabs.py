import logging
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QDialog, QPushButton, QInputDialog, QGridLayout, QComboBox

from .app_wigets import (
    Directories,
    DirWidget,
    ArtistDirsWidget,
    MainButtons,
    FindDuplicatesButtons,
    FindDuplicatesResults,
    AddingButtons,
    LibrariesWidget,
)
from db import DBController
from tag_changer import TagChanger


class MainTab(QWidget):
    def __init__(self, settings):
        """Класс главного окна"""
        super().__init__()
        self.logger = logging.getLogger('App')
        self.settings = settings

        self.tag_changer = TagChanger()

        self.db = DBController()
        with self.db:
            self.db.create_table_if_not_exist()
            self.libraries_list = self.db.get_tables_list()

        # Создание виджетов и макета для их размещения
        self.target_dir_widget = DirWidget(self.settings, Directories.target_dir)
        self.artist_dirs_widget = ArtistDirsWidget(self.settings)
        self.main_button_widget = MainButtons()
        self.main_layout = QVBoxLayout()
        self.create_layout()

    def create_layout(self):
        """Настройка кнопок и макета"""
        self.main_button_widget.readme_button.clicked.connect(self.open_readme)
        self.main_button_widget.reset_settings_button.clicked.connect(self.reset_settings)
        self.main_button_widget.save_settings_button.clicked.connect(self.save_settings)
        self.main_button_widget.start_button.clicked.connect(self.start)

        self.main_button_widget.library_chose_box.addItems(self.libraries_list)

        self.main_layout.addWidget(self.target_dir_widget)
        self.main_layout.addWidget(self.artist_dirs_widget)
        self.main_layout.addWidget(self.main_button_widget)
        self.setLayout(self.main_layout)

    def open_readme(self):
        """Открытие README.md в текстовом редакторе в качестве инструкций и подсказок"""
        self.show_finish_dialog()
        self.logger.info('Открытие README')

    def reset_settings(self):
        """Сброс настроек"""
        self.target_dir_widget.fild.setText('')
        self.artist_dirs_widget.fild.setText('')
        self.settings.clean_main_data()
        self.logger.info('Настройки сброшены')

    def save_settings(self):
        """Сохранение настроек"""
        target_dir = self.target_dir_widget.fild.toPlainText()
        artist_dir = self.artist_dirs_widget.fild.toPlainText()

        self.settings.set_target_dir(target_dir)
        self.settings.set_artist_dir(artist_dir)
        self.settings.save_settings()

        self.logger.info('Настройки сохранены')

    def show_finish_dialog(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Tag Changer')
        dlg.setText('Скрипт завершил работу')
        dlg.exec()

    def start(self):
        """Запуск скрипта"""
        target_dir = self.target_dir_widget.fild.toPlainText()
        artist_dirs = self.artist_dirs_widget.fild.toPlainText()
        db_update = True if self.main_button_widget.db_update_checkbox.checkState() is Qt.CheckState.Checked else False

        self.tag_changer.set_up_target_dir(target_dir)
        self.tag_changer.set_up_artist_dirs(artist_dirs)

        self.logger.info('Запуск скрипта')
        song_datas = self.tag_changer.start(self.tag_changer.target_dir)
        if db_update:
            with self.db:
                self.db.clear_table()
                for song_data in song_datas:
                    self.db.insert(song_data)
        else:
            list(song_datas)

        self.show_finish_dialog()
        self.logger.info('Скрипт завершил работу')


class FindDuplicatesTab(QWidget):
    """
    Виджеты: кнопки; подсказки с тем, заполнена библиотека или нет
    Кнопки: readme, старт
    Ограничения: не должен изменять теги, просто искать дубликаты в уже заполненной библиотеке
    Функционал: нажимаешь на кнопку старта -> показывается список с дубликатами, его можно скролить, дубликаты можно
                выбирать. В окне кнопки 'применить' и 'отменить'. После 'применить' все непомеченные - остаются,
                помеченные - удаляются с диска. Пути ищутся исходя из заданной target_dir и найденных относительных
                путей файлов.
    """
    def __init__(self, settings):
        """Класс главного окна"""
        super().__init__()
        self.logger = logging.getLogger('App')
        self.settings = settings
        self.duplicates = None

        self.db = DBController()
        with self.db:
            self.db.create_table_if_not_exist()

        # Создание виджетов и макета для их размещения
        self.find_duplicates_buttons_widget = FindDuplicatesButtons()
        self.main_layout = QVBoxLayout()
        self.create_layout()

    def create_layout(self):
        """Настройка кнопок и макета"""
        self.find_duplicates_buttons_widget.readme_button.clicked.connect(self.open_readme)
        self.find_duplicates_buttons_widget.start_button.clicked.connect(self.start)

        self.main_layout.addWidget(self.find_duplicates_buttons_widget)
        self.setLayout(self.main_layout)

    def open_readme(self):
        """Открытие README.md в текстовом редакторе в качестве инструкций и подсказок"""
        self.show_finish_dialog()
        self.logger.info('Открытие README')

    def show_finish_dialog(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Результаты')
        dlg.setText('Поиск дубликатов завершён')
        dlg.exec()

    def show_results(self, duplicates):
        dlg = FindDuplicatesDialog(self.settings, self.db, duplicates)
        dlg.exec()

    def start(self):
        """Запуск скрипта"""
        self.logger.info('Запуск скрипта')

        with self.db:
            dup = self.db.find_duplicates()

        self.show_results(dup)
        self.logger.info('Скрипт завершил работу')


class FindDuplicatesDialog(QDialog):
    def __init__(self, settings, db, duplicates: list | tuple):
        super().__init__()
        self.logger = logging.getLogger('App')
        self.settings = settings
        self.duplicates = duplicates
        self.db = db

        self.setFixedSize(QSize(800, 500))
        self.setWindowTitle('Результаты')

        self.main_layout = QVBoxLayout()
        self.duplicates_widget = FindDuplicatesResults(self.duplicates)

        self.create_layout()

    def create_layout(self):
        self.main_layout.addWidget(self.duplicates_widget)
        self.duplicates_widget.ok_button.clicked.connect(self.click_ok)
        self.duplicates_widget.cansel_button.clicked.connect(self.click_cansel)

        self.setLayout(self.main_layout)

    def click_ok(self):
        self.logger.debug('Применить изменения дубликатов')
        items = self.duplicates_widget.get_items_for_delete()
        with self.db:
            for idx, file_path in items:
                self.db.delete(idx)
                full_path = Path(self.settings.target_dir, file_path)
                full_path.unlink(missing_ok=True)
        self.close()

    def click_cansel(self):
        self.logger.debug('Отменить изменения дубликатов')
        self.close()


class AddingTab(QWidget):
    """
    Выбор директории, куда копировать to_dir.
    Выбор директории, откуда копировать from_dir.
    Выбор библиотеки (таблицы в бд), куда заносить изменения library.
    Кнопка для добавления библиотеки. При её нажатии всплывает окошко с вводом текста ->
        текст становится новой таблицей в бд.
    Кнопка для удаления библиотеки. При её нажатии всплывает окошко с выбором библиотеки зи списка.
        Удаляет табличку из бд.
    Кнопка readme.
    Кнопка 'Запуск    >>'.
    Запуск не должен работать, если не заполнены все данные.
    Должен быть пустой выбор в выборе библиотек.
    Попробовать изменить структуру settings, что бы новые разделы были как библиотеки??? - СЛОЖНО, МБ ПОТОМ.
    Не сохранять никаких настроек.
    """
    def __init__(self, settings, db) -> None:
        super().__init__()
        self.logger = logging.getLogger('App')
        self.settings = settings
        self.db = db
        self.to_dir = None
        self.from_dir = None
        self.library = None

        # Создание виджетов и макета для их размещения
        self.libraries_list_widget = LibrariesWidget()
        self.to_dir_widget = DirWidget(settings, Directories.to_dir)
        self.from_dir_widget = DirWidget(settings, Directories.from_dir)
        self.buttons_widget = AddingButtons()
        self.main_layout = QVBoxLayout()
        self.create_layout()

    def create_layout(self):
        with self.db:
            libraries_list = self.db.get_tables_list()
        self.libraries_list_widget.libraries_list.addItem('')
        self.libraries_list_widget.libraries_list.addItems(libraries_list)

        self.libraries_list_widget.add_library_button.clicked.connect(self.open_create_library_dialog)
        self.libraries_list_widget.remove_library_button.clicked.connect(self.open_remove_library_dialog)
        self.to_dir_widget.button.clicked.connect(self.chose_to_dir)
        self.from_dir_widget.button.clicked.connect(self.chose_from_dir)
        self.buttons_widget.readme_button.clicked.connect(self.open_readme)
        self.buttons_widget.start_button.clicked.connect(self.start)

        self.main_layout.addWidget(self.libraries_list_widget)
        self.main_layout.addWidget(self.to_dir_widget)
        self.main_layout.addWidget(self.from_dir_widget)
        self.main_layout.addWidget(self.buttons_widget)
        self.setLayout(self.main_layout)

    def open_create_library_dialog(self):
        dlg = QInputDialog(self)
        dlg.setWindowTitle('Введите название новой библиотеки')

        if dlg.exec():
            library = dlg.textValue()
            if library:
                self.libraries_list_widget.libraries_list.addItem(library)
                # with self.db:
                #     self.db.create_table_if_not_exist(library)

    def open_remove_library_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle('Выберите, какую библиотеку хотите удалить')
        dlg.setFixedSize(QSize(150, 90))
        layout = QGridLayout(dlg)
        chose_library_box = QComboBox()
        ok_button = QPushButton('OK')
        cansel_button = QPushButton('Cansel')
        layout.addWidget(chose_library_box, 0, 0, 0, 2)
        layout.addWidget(ok_button, 2, 0)
        layout.addWidget(cansel_button, 2, 1)
        dlg.exec()
        # items = []
        # for i in range(1, self.libraries_list_widget.libraries_list.count()):
        #     items.append(self.libraries_list_widget.libraries_list.itemText(i))
        # dlg.setComboBoxItems(items)
        #
        # if dlg.exec():
        #     library = dlg.textValue()
        #     if library:
        #         print(library)
        #         self.libraries_list_widget.libraries_list.removeItem()
                # self.libraries_list_widget.libraries_list.addItem(library)
                # with self.db:
                #     self.db.create_table_if_not_exist(library)

    def chose_to_dir(self):
        print('chose to')

    def chose_from_dir(self):
        print('chose from')

    def open_readme(self):
        print('open readme')

    def start(self):
        print('start')
