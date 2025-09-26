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
    SyncLibrariesWidget,
    SyncResult,
    DialogButtons,
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
        self.libraries_widget = LibrariesWidget(self.settings, self.db)
        self.main_button_widget = MainButtons()
        self.main_layout = QVBoxLayout()
        self.create_layout()

    def create_layout(self):
        """Настройка кнопок и макета"""
        self.main_button_widget.readme_button.clicked.connect(self.open_readme)
        self.main_button_widget.reset_settings_button.clicked.connect(self.reset_settings)
        self.main_button_widget.save_settings_button.clicked.connect(self.save_settings)
        self.main_button_widget.start_button.clicked.connect(self.start)

        self.main_layout.addWidget(self.target_dir_widget)
        self.main_layout.addWidget(self.artist_dirs_widget)
        self.main_layout.addWidget(self.libraries_widget)
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
        self.libraries_widget.libraries_list.setCurrentIndex(0)
        self.settings.clean_main_data()

        self.show_info_dialog('Настройки сброшены')
        self.logger.info('Настройки сброшены')

    def save_settings(self):
        """Сохранение настроек"""
        target_dir = self.target_dir_widget.fild.toPlainText()
        artist_dir = self.artist_dirs_widget.fild.toPlainText()
        library = self.libraries_widget.libraries_list.currentText()

        self.settings.set_target_dir(target_dir)
        self.settings.set_artist_dir(artist_dir)
        self.settings.set_current_library(library)
        self.settings.save_settings()

        self.show_info_dialog('Настройки сохранены')
        self.logger.info('Настройки сохранены')

    def show_info_dialog(self, msg: str = 'Произошло что-то неожиданное'):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Tag Changer')
        dlg.setText(msg)
        dlg.exec()

    def start(self):
        """Запуск скрипта"""
        target_dir = self.target_dir_widget.fild.toPlainText()
        artist_dirs = self.artist_dirs_widget.fild.toPlainText().split('\n')
        library = self.libraries_widget.libraries_list.currentText()
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
        self.target_dir_widget = DirWidget(self.settings, Directories.target_dir)
        self.libraries_widget = LibrariesWidget(self.settings, self.db)
        self.find_duplicates_buttons_widget = FindDuplicatesButtons()
        self.main_layout = QVBoxLayout()
        self.create_layout()

    def create_layout(self):
        """Настройка кнопок и макета"""
        self.find_duplicates_buttons_widget.readme_button.clicked.connect(self.open_readme)
        self.find_duplicates_buttons_widget.start_button.clicked.connect(self.start)

        self.main_layout.addWidget(self.target_dir_widget)
        self.main_layout.addWidget(self.libraries_widget)
        self.main_layout.addWidget(self.find_duplicates_buttons_widget)
        self.setLayout(self.main_layout)

    def open_readme(self):
        """Открытие README.md в текстовом редакторе в качестве инструкций и подсказок"""
        self.show_info_dialog('Открытие README')
        self.logger.info('Открытие README')

    def show_info_dialog(self, msg: str = 'Произошло что-то неожиданное'):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Поиск дубликатов')
        dlg.setText(msg)
        dlg.exec()

    def show_results(self, duplicates, library):
        dlg = FindDuplicatesDialog(self.target_dir_widget.fild.toPlainText(), self.db, duplicates, library)
        dlg.exec()

    def start(self):
        """Запуск скрипта"""
        self.logger.info('Запуск скрипта')

        library = self.libraries_widget.libraries_list.currentText()
        if not library:
            self.show_info_dialog('Выберите библиотеку')
            return 1

        with self.db:
            duplicates = self.db.find_duplicates(library)

        self.show_results(duplicates, library)
        self.logger.info('Скрипт завершил работу')


class FindDuplicatesDialog(QDialog):
    def __init__(self, target_dir: str, db: DBController, duplicates: list | tuple, library: str):
        super().__init__()
        self.logger = logging.getLogger('App')
        self.target_dir = target_dir
        self.db = db

        self.duplicates = duplicates
        self.library = library

        self.setFixedSize(QSize(800, 500))
        self.setWindowTitle('Результаты')

        self.main_layout = QVBoxLayout()
        self.duplicates_widget = FindDuplicatesResults(self.duplicates)

        self.create_layout()

    def create_layout(self):
        self.duplicates_widget.ok_button.clicked.connect(self.click_ok)
        self.duplicates_widget.cansel_button.clicked.connect(self.click_cansel)

        self.main_layout.addWidget(self.duplicates_widget)
        self.setLayout(self.main_layout)

    def click_ok(self):
        self.logger.debug('Применить изменения дубликатов')
        items = self.duplicates_widget.get_items_for_delete()
        with self.db:
            for idx, file_path in items:
                self.db.delete(idx, self.library)
                full_path = Path(self.target_dir, file_path)
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
        self.libraries_widget = LibrariesWidget(self.settings, self.db)
        self.to_dir_widget = DirWidget(self.settings, Directories.to_dir)
        self.from_dir_widget = DirWidget(self.settings, Directories.from_dir)
        self.buttons_widget = ExpansionButtons()
        self.main_layout = QVBoxLayout()
        self.create_layout()

    def create_layout(self):
        self.buttons_widget.readme_button.clicked.connect(self.open_readme)
        self.buttons_widget.start_button.clicked.connect(self.start)

        self.main_layout.addWidget(self.libraries_widget)
        self.main_layout.addWidget(self.to_dir_widget)
        self.main_layout.addWidget(self.from_dir_widget)
        self.main_layout.addWidget(self.buttons_widget)
        self.setLayout(self.main_layout)

    def open_readme(self):
        pass

    def start(self):
        library = self.libraries_widget.libraries_list.currentText()
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


class SynchronizationTab(QWidget):
    def __init__(self, settings: Settings, db: DBController):
        super().__init__()
        self.settings = settings
        self.db = db

        self.sync1_dir_widget = DirWidget(self.settings, Directories.sync1_dir)
        self.sync2_dir_widget = DirWidget(self.settings, Directories.sync2_dir)
        self.sync_libraries_widget = SyncLibrariesWidget(self.settings, self.db)
        self.buttons_widget = MainButtons(is_sync_tab=True)

        self.main_layout = QVBoxLayout()
        self.create_layout()

    def create_layout(self):
        self.buttons_widget.readme_button.clicked.connect(self.open_readme)
        self.buttons_widget.reset_settings_button.clicked.connect(self.reset_settings)
        self.buttons_widget.save_settings_button.clicked.connect(self.save_settings)
        self.buttons_widget.start_button.clicked.connect(self.start)

        self.main_layout.addWidget(self.sync1_dir_widget)
        self.main_layout.addWidget(self.sync2_dir_widget)
        self.main_layout.addWidget(self.sync_libraries_widget)
        self.main_layout.addWidget(self.buttons_widget)

        self.setLayout(self.main_layout)

    def show_info_dialog(self, msg: str = 'Произошло что-то неожиданное'):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Синхронизация')
        dlg.setText(msg)
        dlg.exec()

    def open_readme(self):
        self.show_info_dialog('Open README')

    def reset_settings(self):
        """Сброс настроек"""
        self.sync1_dir_widget.fild.setText('')
        self.sync2_dir_widget.fild.setText('')
        self.sync_libraries_widget.sync1_library_list.setCurrentIndex(0)
        self.sync_libraries_widget.sync2_library_list.setCurrentIndex(0)
        self.settings.clean_sync_data()

        self.show_info_dialog('Настройки сброшены')

    def save_settings(self):
        """Сохранение настроек"""
        dir1 = self.sync1_dir_widget.fild.toPlainText()
        dir2 = self.sync2_dir_widget.fild.toPlainText()
        library1 = self.sync_libraries_widget.sync1_library_list.currentText()
        library2 = self.sync_libraries_widget.sync2_library_list.currentText()

        self.settings.set_sync1_dir(dir1)
        self.settings.set_sync2_dir(dir2)
        self.settings.set_sync1_library(library1)
        self.settings.set_sync2_library(library2)
        self.settings.save_settings()

        self.show_info_dialog('Настройки сохранены')

    def start(self):
        dir1 = self.sync1_dir_widget.fild.toPlainText()
        dir2 = self.sync2_dir_widget.fild.toPlainText()
        library1 = self.sync_libraries_widget.sync1_library_list.currentText()
        library2 = self.sync_libraries_widget.sync2_library_list.currentText()

        dlg = SyncDialog(dir1, dir2, library1, library2)
        dlg.exec()


class SyncDialog(QDialog):
    def __init__(self, dir1: str, dir2: str, library1: str, library2: str):
        super().__init__()

        self.dir1 = dir1
        self.dir2 = dir2
        self.library1 = library1
        self.library2 = library2

        self.result1_widget = QWidget()
        self.result2_widget = QWidget()
        self.buttons_widget = DialogButtons()

        self.create_layout()

    def create_layout(self):
        self.setFixedSize(QSize(800, 500))
        self.setWindowTitle('Синхронизация')

        layout = QVBoxLayout()
        layout.addWidget(self.result1_widget)
        layout.addWidget(self.result2_widget)
        layout.addWidget(self.buttons_widget)

        self.setLayout(layout)

