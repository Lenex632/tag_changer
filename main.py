import configparser
import logging
from pathlib import Path
import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget

from app import MainTab, FindDuplicatesTab, AddingTab
from db import DBController


# TODO
#       Сделать file_path в бд уникальным, что бы по нему нельзя было создавать записи в бд при "Добавлении".
#       "Добавление" - Есть папка from_dir, есть папка to_dir. Обрабатывать from_dir -> копировать в to_dir (либо просто
#     копировать) -> обновлять бд (либо обновлять прямо во время копирования). Возможно сделать просто как галочку с
#     возможностью выбрать from_dir. После завершения копирования - очищать from_dir, но не трогать структуру
#       Next:
#               "Добавление": создать таб, создать виджет
#               "Синхронизация"
#               Добавить возможность добавлять и удалять библиотеки (таблицы в бд)
class Settings:
    def __init__(self):
        """Класс для работы с файлом настроек и конфигураций"""
        self._settings = configparser.ConfigParser()
        self.path = Path(Path(__file__).parent, 'settings.ini')
        if not self.path.exists():
            self.path.touch()
        self._settings.read(self.path)

        self.target_dir = None
        self.artist_dirs = None
        self.to_dir = None
        self.from_dir = None
        self.sync_dir = None
        self.target_sync_dir = None
        self.set_defaults()

    def set_defaults(self) -> None:
        """Настраивает дефолтные значения из settings.ini при запуске программы"""
        if not self._settings.has_section('main'):
            self._settings.add_section('main')

        self.target_dir = self._settings.get(section='main', option='target_dir', fallback=None)
        self.artist_dirs = self._settings.get(section='main', option='artist_dirs', fallback='').split('\n')
        self.sync_dir = self._settings.get(section='settings', option='sync_dir', fallback='')
        self.target_sync_dir = self._settings.get(section='settings', option='sync_dir', fallback='')
        self.to_dir = ''
        self.from_dir = ''

    def set_target_dir(self, value) -> None:
        """Настраивает значение target_dir"""
        self._settings.set(section='main', option='target_dir', value=value)
        self.target_dir = value

    def set_artist_dir(self, value) -> None:
        """Настраивает значение artist_dirs"""
        self._settings.set(section='main', option='artist_dirs', value=value)
        self.artist_dirs = value

    def set_sync_dir(self, value) -> None:
        """Настраивает значение sync_dir"""
        self._settings.set(section='sync', option='sync_dir', value=value)
        self.artist_dirs = value

    def set_target_sync_dir(self, value) -> None:
        """Настраивает значение target_sync_dir"""
        self._settings.set(section='sync', option='target_sync_dir', value=value)
        self.artist_dirs = value

    def save_settings(self) -> None:
        """Сохраняет настройки в файл settings.ini"""
        with open(self.path, 'w') as file:
            self._settings.write(file)

    def clean_main_data(self) -> None:
        """Сбрасывает настройки и сохраняет их в файл"""
        self.set_target_dir('')
        self.set_artist_dir('')
        self.save_settings()

    def clean_sync_data(self) -> None:
        """Сбрасывает настройки и сохраняет их в файл"""
        self.set_sync_dir('')
        self.set_target_sync_dir('')
        self.save_settings()


class MainWindow(QMainWindow):
    def __init__(self):
        """Класс главного окна"""
        super().__init__()

        self.logger = logging.getLogger('App')
        self.settings = Settings()
        self.db = DBController()
        self.set_window_parameters()

    def set_window_parameters(self):
        """Настройка параметров окна"""
        self.setWindowTitle('Tag Changer')
        self.setFixedSize(QSize(800, 500))

        # Создание и размещение вкладок
        tabs = QTabWidget()
        tabs.addTab(MainTab(self.settings), 'Изменение тегов')
        tabs.addTab(AddingTab(self.settings, self.db), 'Добавление')
        tabs.addTab(FindDuplicatesTab(self.settings), 'Поиск дубликатов')
        tabs.addTab(QWidget(), 'Синхронизация')

        self.setCentralWidget(tabs)

        self.show()


if __name__ == '__main__':
    from logger import set_up_logger_config
    set_up_logger_config()

    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
