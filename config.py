import configparser
import json
import logging
import shutil

from pathlib import Path


class AppConfig:
    def __init__(self) -> None:
        """Класс для работы с файлом настроек и конфигураций"""
        self.logger = logging.getLogger('Config')
        self.config = configparser.ConfigParser()
        self.path = Path(Path(__file__).parent, 'settings.ini')
        self.default = Path(Path(__file__).parent, 'settings_example.ini')
        if not self.path.exists():
            shutil.copy(self.default, self.path)
        self.config.read(self.path, encoding='utf-8')

    def update(self) -> None:
        with open(self.path, 'w', encoding='utf-8') as f:
            self.config.write(f)

    @property
    def target_dir(self) -> str:
        return self.config['main']['target_dir']

    @target_dir.setter
    def target_dir(self, value: str) -> None:
        self.config['main']['target_dir'] = value

    @property
    def artist_dir(self) -> list:
        return json.loads(self.config['main']['artist_dir'])

    @artist_dir.setter
    def artist_dir(self, value: list) -> None:
        self.config['main']['artist_dir'] = json.dumps(value)

    @property
    def library(self) -> str:
        return self.config['main']['library']

    @library.setter
    def library(self, value: str) -> None:
        self.config['main']['library'] = value

    @property
    def update_lib(self) -> bool:
        return self.config['main'].getboolean('update_lib')

    @update_lib.setter
    def update_lib(self, value: bool) -> None:
        self.config['main']['update_lib'] = str(value)

    @property
    def to_dir(self) -> str:
        return self.config['add']['to_dir']

    @to_dir.setter
    def to_dir(self, value: str) -> None:
        self.config['add']['to_dir'] = value

    @property
    def from_dir(self) -> str:
        return self.config['add']['from_dir']

    @from_dir.setter
    def from_dir(self, value: str) -> None:
        self.config['add']['from_dir'] = value

    @property
    def add_lib(self) -> str:
        return self.config['add']['add_lib']

    @add_lib.setter
    def add_lib(self, value: str) -> None:
        self.config['add']['add_lib'] = value

    @property
    def duplicates_dir(self) -> str:
        return self.config['duplicates']['duplicates_dir']

    @duplicates_dir.setter
    def duplicates_dir(self, value: str) -> None:
        self.config['duplicates']['duplicates_dir'] = value

    @property
    def duplicates_lib(self) -> str:
        return self.config['duplicates']['duplicates_lib']

    @duplicates_lib.setter
    def duplicates_lib(self, value: str) -> None:
        self.config['duplicates']['duplicates_lib'] = value

    @property
    def sync_dir_1(self) -> str:
        return self.config['sync']['sync_dir_1']

    @sync_dir_1.setter
    def sync_dir_1(self, value: str) -> None:
        self.config['sync']['sync_dir_1'] = value

    @property
    def sync_dir_2(self) -> str:
        return self.config['sync']['sync_dir_2']

    @sync_dir_2.setter
    def sync_dir_2(self, value: str) -> None:
        self.config['sync']['sync_dir_2'] = value

    @property
    def sync_lib_1(self) -> str:
        return self.config['sync']['sync_lib_1']

    @sync_lib_1.setter
    def sync_lib_1(self, value: str) -> None:
        self.config['sync']['sync_lib_1'] = value

    @property
    def sync_lib_2(self) -> str:
        return self.config['sync']['sync_lib_2']

    @sync_lib_2.setter
    def sync_lib_2(self, value: str) -> None:
        self.config['sync']['sync_lib_2'] = value


def test_main():
    config = AppConfig()
    print(config.target_dir)
    config.target_dir = ''
    print(config.update_lib)
    config.update_lib = False
    print(config.update_lib)
    print(config.artist_dir)
    config.artist_dir = ['1', '2']
    config.artist_dir = ['Legend', 'Легенды']
    config.update()


if __name__ == "__main__":
    from logger import set_up_logger_config
    set_up_logger_config()

    test_main()

