import configparser
import logging
from pathlib import Path


class Settings:
    def __init__(self):
        """Класс для работы с файлом настроек и конфигураций"""
        self.logger = logging.getLogger('Settings')
        self._settings = configparser.ConfigParser()
        self.path = Path(Path(__file__).parent, 'settings.ini')
        if not self.path.exists():
            self.path.touch()
        self._settings.read(self.path)

        self.target_dir = None
        self.artist_dirs = None
        self.current_library = None
        self.to_dir = ''
        self.from_dir = ''
        self.sync_dir = None
        self.target_sync_dir = None
        self.set_defaults()

    def set_defaults(self) -> None:
        """Настраивает дефолтные значения из settings.ini при запуске программы"""
        if not self._settings.has_section('main'):
            self._settings.add_section('main')

        self.target_dir = self._settings.get(section='main', option='target_dir', fallback=None)
        self.artist_dirs = self._settings.get(section='main', option='artist_dirs', fallback='').split('\n')

        self.current_library = self._settings.get(section='libraries', option='current_library', fallback='')

        self.sync_dir = self._settings.get(section='settings', option='sync_dir', fallback='')
        self.target_sync_dir = self._settings.get(section='settings', option='sync_dir', fallback='')

    def set_target_dir(self, value: str) -> None:
        """Настраивает значение target_dir"""
        self._settings.set(section='main', option='target_dir', value=value)
        self.target_dir = value

    def set_artist_dir(self, value: str) -> None:
        """Настраивает значение artist_dirs"""
        self._settings.set(section='main', option='artist_dirs', value=value)
        self.artist_dirs = value

    def set_current_library(self, value: str) -> None:
        """Настраивает значение current_library"""
        self._settings.set(section='libraries', option='current_library', value=value)
        self.current_library = value

    def set_sync_dir(self, value: str) -> None:
        """Настраивает значение sync_dir"""
        self._settings.set(section='sync', option='sync_dir', value=value)
        self.artist_dirs = value

    def set_target_sync_dir(self, value: str) -> None:
        """Настраивает значение target_sync_dir"""
        self._settings.set(section='sync', option='target_sync_dir', value=value)
        self.artist_dirs = value

    def save_settings(self) -> None:
        """Сохраняет настройки в файл settings.ini"""
        with open(self.path, 'w') as file:
            self._settings.write(file)

    def clean_main_data(self) -> None:
        """Сбрасывает главные настройки и сохраняет их в файл"""
        self.set_target_dir('')
        self.set_artist_dir('')
        self.set_current_library('')
        self.save_settings()

    def clean_sync_data(self) -> None:
        """Сбрасывает настройки и сохраняет их в файл"""
        self.set_sync_dir('')
        self.set_target_sync_dir('')
        self.save_settings()
