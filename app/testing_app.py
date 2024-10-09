import configparser
import logging
from pathlib import Path
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QCheckBox,
)

from tag_changer.tag_changer import TagChanger
from db.db_controller import DBController


class Settings:
    def __init__(self):
        """Класс для работы с файлом настроек и конфигураций"""
        self._settings = configparser.ConfigParser()
        self.path = Path(Path(__file__).parent.parent, 'settings.ini')
        if self.path:
            self._settings.read(self.path)

        self.target_dir = None
        self.artist_dirs = None
        self.set_defaults()

    def set_defaults(self) -> None:
        """Настраивает дефолтные значения из settings.ini при запуске программы"""
        self.target_dir = self._settings.get(section='settings', option='target_dir', fallback=None)
        self.artist_dirs = self._settings.get(section='settings', option='artist_dirs', fallback='').split('\n')

    def set_target_dir(self, value) -> None:
        """Настраивает значение target_dir"""
        self._settings.set(section='settings', option='target_dir', value=value)
        self.target_dir = value

    def set_artist_dir(self, value) -> None:
        """Настраивает значение artist_dirs"""
        self._settings.set(section='settings', option='artist_dirs', value=value)
        self.artist_dirs = value

    def save_settings(self) -> None:
        """Сохраняет настройки в файл settings.ini"""
        with open(self.path, 'w') as file:
            self._settings.write(file)

    def clean_data(self) -> None:
        """Сбрасывает настройки и сохраняет их в файл"""
        self.set_target_dir('')
        self.set_artist_dir('')
        self.save_settings()


class TargetDir(QWidget):
    def __init__(self, settings):
        """Класс для работы с полем для ввода target_dir"""
        super().__init__()
        self.settings = settings
        self.placeholder = 'Укажите путь к исходной папке'

        self.label = QLabel(self.placeholder)
        self.button = self.create_button()
        self.fild = self.create_fild()

        self.create_layout()

    def create_button(self) -> QPushButton:
        """Создаёт кнопку для выбора директории в общем пространстве"""
        button = QPushButton('O')
        button.clicked.connect(self.click_button)

        return button

    def click_button(self) -> None:
        """Создаёт диалог с поиском директории в общем пространстве и возвращает полученное значение"""
        dialog = QFileDialog()
        dialog.setWindowTitle(self.placeholder)
        chosen_dir = dialog.getExistingDirectory()
        self.fild.setText(chosen_dir)

    def create_fild(self) -> QTextEdit:
        """Создаёт поле в которое будет записываться значение target_dir"""
        fild = QTextEdit()
        fild.setPlaceholderText(self.placeholder)
        if self.settings.target_dir:
            fild.setText(self.settings.target_dir)

        return fild

    def create_layout(self) -> None:
        """Создаёт виджет для размещения в окне"""
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.button)
        bottom_layout.addWidget(self.fild)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)


class ArtistDirs(QWidget):
    def __init__(self, settings):
        """Класс для работы с полем для ввода artist_dir"""
        super().__init__()
        self.settings = settings
        self.placeholder = 'Укажите папки с исполнителями для Уровня 2 (каждый с новой строки)'

        self.label = QLabel(self.placeholder)
        self.fild = self.create_fild()

        self.create_layout()

    def create_fild(self) -> QTextEdit:
        """Создаёт поле в которое будет записываться значение artist_dir"""
        fild = QTextEdit()
        fild.setPlaceholderText(self.placeholder)
        if self.settings.artist_dirs:
            text = '\n'.join(self.settings.artist_dirs)
            fild.setText(text)

        return fild

    def create_layout(self) -> None:
        """Создаёт виджет для размещения в окне"""
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.fild)

        self.setLayout(layout)


class MainButton(QWidget):
    def __init__(self, settings):
        """Класс для работы с кнопками в главном окне"""
        super().__init__()
        self.settings = settings

        self.sync_checkbox = QCheckBox('Синхронизация')
        self.readme_button = QPushButton('Открыть ReadMe')
        self.reset_settings_button = QPushButton('Сбросить настройки')
        self.save_settings_button = QPushButton('Сохранить настройки')
        self.start_button = QPushButton('Запуск   >>')

        self.create_layout()

    def create_layout(self):
        """Создаёт виджет для размещения в окне"""
        layout = QGridLayout()
        layout.addWidget(self.sync_checkbox, 0, 0)
        layout.addWidget(self.readme_button, 1, 0)
        layout.addWidget(self.reset_settings_button, 2, 0)
        layout.addWidget(self.save_settings_button, 2, 1)
        layout.addWidget(self.start_button, 2, 2)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        """Класс главного окна"""
        super().__init__()

        self.logger = logging.getLogger('App')

        self.settings = Settings()
        self.tag_changer = TagChanger()
        self.db = DBController()
        self.set_window_parameters()

        # Создание виджетов
        self.target_dir_widget = TargetDir(self.settings)
        self.artist_dirs_widget = ArtistDirs(self.settings)
        self.main_button_widget = MainButton(self.settings)

        # Размещение виджетов
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.target_dir_widget)
        self.main_layout.addWidget(self.artist_dirs_widget)
        self.main_layout.addWidget(self.main_button_widget)
        self.set_up_buttons()

        # Создание и размещение главного виджета
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

        self.show()

    def set_window_parameters(self):
        """Настройка параметров окна"""
        self.setWindowTitle('Tag Changer')
        self.setFixedSize(QSize(800, 500))

    def set_up_buttons(self):
        """Настройка кнопок привязка их к исполняемым функциям"""
        self.main_button_widget.readme_button.clicked.connect(self.open_readme)
        self.main_button_widget.reset_settings_button.clicked.connect(self.reset_settings)
        self.main_button_widget.save_settings_button.clicked.connect(self.save_settings)
        self.main_button_widget.start_button.clicked.connect(self.start)

    def open_readme(self):
        """Открытие README.md в текстовом редакторе в качестве инструкций и подсказок"""
        self.logger.info('Открытие README')

    def reset_settings(self):
        """Сброс настроек"""
        self.target_dir_widget.fild.setText('')
        self.artist_dirs_widget.fild.setText('')
        self.settings.clean_data()
        self.logger.info('Настройки сброшены')

    def save_settings(self):
        """Сохранение настроек"""
        target_dir = self.target_dir_widget.fild.toPlainText()
        artist_dir = self.artist_dirs_widget.fild.toPlainText()

        self.settings.set_target_dir(target_dir)
        self.settings.set_artist_dir(artist_dir)
        self.settings.save_settings()

        self.logger.info('Настройки сохранены')

    def start(self):
        """Запуск скрипта"""
        target_dir = self.target_dir_widget.fild.toPlainText()
        artist_dirs = self.artist_dirs_widget.fild.toPlainText()
        need_to_sync = True if self.main_button_widget.sync_checkbox.checkState() is Qt.CheckState.Checked else False

        self.tag_changer.set_up_target_dir(target_dir)
        self.tag_changer.set_up_artist_dirs(artist_dirs)

        self.logger.info('Запуск скрипта')
        song_datas = self.tag_changer.start(self.tag_changer.target_dir)
        if need_to_sync:
            self.db.clear_table()
        else:
            list(song_datas)
        self.logger.info('Скрипт завершил работу')


if __name__ == '__main__':
    from logger import set_up_logger_config
    set_up_logger_config()

    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
