import logging
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QDialog

from app.app_wigets import (
    Directories,
    DirWidget,
    ArtistDirsWidget,
    MainButtons,
    FindDuplicatesButtons,
    FindDuplicatesResults,
)
from db.db_controller import DBController
from model import SongData
from tag_changer.tag_changer import TagChanger


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

        # Создание виджетов и макета для их размещения
        self.target_dir_widget = DirWidget(self.settings, Directories.target_dir)
        self.artist_dirs_widget = ArtistDirsWidget(self.settings)
        self.main_button_widget = MainButtons()
        self.main_layout = QVBoxLayout()
        self.set_up_layout()

    def set_up_layout(self):
        """Настройка кнопок и макета"""
        self.main_button_widget.readme_button.clicked.connect(self.open_readme)
        self.main_button_widget.reset_settings_button.clicked.connect(self.reset_settings)
        self.main_button_widget.save_settings_button.clicked.connect(self.save_settings)
        self.main_button_widget.start_button.clicked.connect(self.start)

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


class FinDuplicatesTab(QWidget):
    """
    Виджеты: кнопки; подсказки с тем, заполнена библиотека или нет
    Кнопки: readme, старт
    Ограничения: не должен изменять теги, просто искать дубликаты в уже заполненной библиотеке
    Функционал: нажимаешь на кнопку старта -> показывается список с дубликатами, го можно скролить, дубликаты можно
                выбирать и проставлять метки '+' или '-', по умолчанию '+'. В окне кнопки 'применить' и 'отменить'.
                После 'применить' все с '+' - остаются, все с '-' - удаляются с диска. Пути ищутся исходя из заданной
                target_dir и найденных относительных путей файлов.

    МБ:
        Искать не в заполненной библиотеке, а в папке, но просто проходится по ней аналогом tag_changer, который будет
        просто сканировать папку и записывать теги песен в бд.
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
        self.set_up_layout()

    def set_up_layout(self):
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
        dlg = QDialog(self)
        dlg.setFixedSize(QSize(800, 500))
        dlg.setWindowTitle('Результаты')
        layout = QVBoxLayout()
        layout.addWidget(FindDuplicatesResults(self.settings.target_dir, duplicates))
        dlg.setLayout(layout)
        dlg.exec()

    def start(self):
        """Запуск скрипта"""
        self.logger.info('Запуск скрипта')

        with self.db:
            dup = self.db.find_duplicates()

        self.show_results(dup)
        self.logger.info('Скрипт завершил работу')
