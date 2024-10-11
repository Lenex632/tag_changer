import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox

from tag_changer.tag_changer import TagChanger
from db.db_controller import DBController
from app.app_wigets import Directories, DirWidget, ArtistDirsWidget, MainButtons


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
        self.main_button_widget = MainButtons(self.settings)
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
    def __init__(self, settings):
        """Класс главного окна"""
        super().__init__()
        self.logger = logging.getLogger('App')
        self.settings = settings

        self.db = DBController()
        with self.db:
            self.db.create_table_if_not_exist()

        # Создание виджетов и макета для их размещения
        self.main_layout = QVBoxLayout()
        self.set_up_layout()

    def set_up_layout(self):
        """Настройка кнопок и макета"""
        self.setLayout(self.main_layout)

    def open_readme(self):
        """Открытие README.md в текстовом редакторе в качестве инструкций и подсказок"""
        self.show_finish_dialog()
        self.logger.info('Открытие README')

    def show_finish_dialog(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Tag Changer')
        dlg.setText('Скрипт завершил работу')
        dlg.exec()

    def start(self):
        """Запуск скрипта"""
        target_dir = self.target_dir_widget.fild.toPlainText()

        self.logger.info('Запуск скрипта')

        self.show_finish_dialog()
        self.logger.info('Скрипт завершил работу')
