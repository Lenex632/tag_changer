import logging
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QDialog

from .app_wigets import (
    Directories,
    DirWidget,
    ArtistDirsWidget,
    MainButtons,
    FindDuplicatesButtons,
    FindDuplicatesResults,
    ExpansionButtons,
    LibrariesWidget,
)
from db import DBController
from tag_changer import TagChanger
from settings import Settings


class MainTab(QWidget):
    def __init__(self, settings: Settings, db: DBController):
        """Класс главного окна"""
        super().__init__()
        self.logger = logging.getLogger('App')
        self.settings = settings
        self.tag_changer = TagChanger()
        self.db = db

        # Создание виджетов и макета для их размещения
        self.target_dir_widget = DirWidget(self.settings, Directories.target_dir)
        self.artist_dirs_widget = ArtistDirsWidget(self.settings)
        self.libraries_list_widget = LibrariesWidget(self.settings, self.db)
        self.main_button_widget = MainButtons()
        self.main_layout = QVBoxLayout()
        self.create_layout()

    def create_layout(self):
        """Настройка кнопок и макета"""
        self.libraries_list_widget.libraries_list.setCurrentText(self.settings.current_library)

        self.main_button_widget.readme_button.clicked.connect(self.open_readme)
        self.main_button_widget.reset_settings_button.clicked.connect(self.reset_settings)
        self.main_button_widget.save_settings_button.clicked.connect(self.save_settings)
        self.main_button_widget.start_button.clicked.connect(self.start)

        self.main_layout.addWidget(self.target_dir_widget)
        self.main_layout.addWidget(self.artist_dirs_widget)
        self.main_layout.addWidget(self.libraries_list_widget)
        self.main_layout.addWidget(self.main_button_widget)
        self.setLayout(self.main_layout)

    def open_readme(self):
        """Открытие README.md в текстовом редакторе в качестве инструкций и подсказок"""
        self.show_info_dialog('Открытие README')
        self.logger.info('Открытие README')

    def reset_settings(self):
        """Сброс настроек"""
        self.target_dir_widget.fild.setText('')
        self.artist_dirs_widget.fild.setText('')
        self.libraries_list_widget.libraries_list.setCurrentIndex(0)
        self.settings.clean_main_data()
        self.logger.info('Настройки сброшены')

    def save_settings(self):
        """Сохранение настроек"""
        target_dir = self.target_dir_widget.fild.toPlainText()
        artist_dir = self.artist_dirs_widget.fild.toPlainText()
        library = self.libraries_list_widget.libraries_list.currentText()

        self.settings.set_target_dir(target_dir)
        self.settings.set_artist_dir(artist_dir)
        self.settings.set_current_library(library)
        self.settings.save_settings()

        self.logger.info('Настройки сохранены')

    def show_info_dialog(self, msg: 'Произошло что-то неожиданное'):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Tag Changer')
        dlg.setText(msg)
        dlg.exec()

    def start(self):
        """Запуск скрипта"""
        self.save_settings()
        target_dir = self.settings.target_dir
        artist_dirs = self.settings.artist_dirs
        library = self.settings.current_library
        db_update = True if self.main_button_widget.db_update_checkbox.checkState() is Qt.CheckState.Checked else False

        if not target_dir or (not library and db_update):
            self.show_info_dialog('Не все данные были заполнены')
            return 1

        self.tag_changer.set_up_target_dir(target_dir)
        self.tag_changer.set_up_artist_dirs(artist_dirs)

        self.logger.info('Запуск скрипта')
        song_datas = self.tag_changer.start(self.tag_changer.target_dir)
        if db_update:
            with self.db:
                self.db.clear_table(library)
                for song_data in song_datas:
                    self.db.insert(song_data, library)
        else:
            list(song_datas)

        self.show_info_dialog('Скрипт завершил работу')
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
    def __init__(self, settings: Settings, db: DBController):
        """Класс главного окна"""
        super().__init__()
        self.logger = logging.getLogger('App')
        self.settings = settings
        self.duplicates = None

        self.db = db

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
            # TODO дописать libraries
            dup = self.db.find_duplicates()

        self.show_results(dup)
        self.logger.info('Скрипт завершил работу')


class FindDuplicatesDialog(QDialog):
    def __init__(self, settings: Settings, db: DBController, duplicates: list | tuple):
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
                # TODO дописать library
                self.db.delete(idx)
                full_path = Path(self.settings.target_dir, file_path)
                full_path.unlink(missing_ok=True)
        self.close()

    def click_cansel(self):
        self.logger.debug('Отменить изменения дубликатов')
        self.close()


class ExpansionTab(QWidget):
    def __init__(self, settings: Settings, db: DBController) -> None:
        super().__init__()
        self.logger = logging.getLogger('App')
        self.settings = settings
        self.db = db
        self.tag_changer = TagChanger()

        # Создание виджетов и макета для их размещения
        self.libraries_list_widget = LibrariesWidget(self.settings, self.db)
        self.to_dir_widget = DirWidget(settings, Directories.to_dir)
        self.from_dir_widget = DirWidget(settings, Directories.from_dir)
        self.buttons_widget = ExpansionButtons()
        self.main_layout = QVBoxLayout()
        self.create_layout()

    def create_layout(self):
        self.buttons_widget.readme_button.clicked.connect(self.open_readme)
        self.buttons_widget.start_button.clicked.connect(self.start)

        self.main_layout.addWidget(self.libraries_list_widget)
        self.main_layout.addWidget(self.to_dir_widget)
        self.main_layout.addWidget(self.from_dir_widget)
        self.main_layout.addWidget(self.buttons_widget)
        self.setLayout(self.main_layout)

    def open_readme(self):
        pass

    def start(self):
        library = self.libraries_list_widget.libraries_list.currentText()
        to_dir = self.to_dir_widget.fild.toPlainText()
        from_dir = self.from_dir_widget.fild.toPlainText()
        artist_dirs = self.settings.artist_dirs

        if not library or not to_dir or not from_dir or not artist_dirs:
            dlg = QMessageBox(self)
            dlg.setText('Не все данные были заполнены')
            return dlg.exec()

        self.tag_changer.set_up_target_dir(from_dir)
        self.tag_changer.artist_dirs = artist_dirs

        self.logger.info('Запуск скрипта')
        song_datas = self.tag_changer.start(self.tag_changer.target_dir)
        with self.db:
            for song_data in song_datas:
                self.db.insert(song_data, library)

                from_path = Path(from_dir, song_data.file_path)
                to_path = Path(to_dir, song_data.file_path)
                to_path.parent.mkdir(parents=True, exist_ok=True)
                from_path.rename(to_path)
