import configparser
from pathlib import Path
import sys

from PyQt6.QtCore import QSize
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
)


class Settings:
    def __init__(self):
        self._settings = configparser.ConfigParser()
        self.path = Path(Path(__file__).parent.parent, 'settings.ini')
        if self.path:
            self._settings.read(self.path)

        self.target_dir = None
        self.artist_dirs = None
        self.set_defaults()

    def set_defaults(self) -> None:
        self.target_dir = self._settings.get(section='settings', option='target_dir', fallback=None)
        self.artist_dirs = self._settings.get(section='settings', option='artist_dirs', fallback='').split('\n')

    def set_target_dir(self, value) -> None:
        self._settings.set(section='settings', option='target_dir', value=value)
        self.target_dir = value

    def set_artist_dir(self, value) -> None:
        self._settings.set(section='settings', option='artist_dirs', value=value)
        self.artist_dirs = value

    def save_settings(self) -> None:
        with open(self.path, 'w') as file:
            self._settings.write(file)

    def clean_data(self) -> None:
        self.set_target_dir('')
        self.set_artist_dir('')
        self.save_settings()


class TargetDir(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.placeholder = 'Укажите путь к исходной папке'

        self.label = QLabel(self.placeholder)
        self.button = self.create_button()
        self.fild = self.create_fild()

        self.create_layout()

    def create_button(self) -> QPushButton:
        button = QPushButton('O')
        button.clicked.connect(self.click_button)

        return button

    def click_button(self) -> None:
        dialog = QFileDialog()
        dialog.setWindowTitle(self.placeholder)
        chosen_dir = dialog.getExistingDirectory()
        self.fild.setText(chosen_dir)

    def create_fild(self) -> QTextEdit:
        fild = QTextEdit()
        fild.setPlaceholderText(self.placeholder)
        if self.settings.target_dir:
            fild.setText(self.settings.target_dir)

        return fild

    def create_layout(self) -> None:
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.button)
        bottom_layout.addWidget(self.fild)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)


class ArtistDirs(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.placeholder = 'Укажите папки с исполнителями для Уровня 2 (каждый с новой строки)'

        self.label = QLabel(self.placeholder)
        self.fild = self.create_fild()

        self.create_layout()

    def create_fild(self) -> QTextEdit:
        fild = QTextEdit()
        fild.setPlaceholderText(self.placeholder)
        if self.settings.artist_dirs:
            text = '\n'.join(self.settings.artist_dirs)
            fild.setText(text)

        return fild

    def create_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.fild)

        self.setLayout(layout)


class MainButton(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings

        self.readme_button = self.create_button('Открыть ReadMe', self.open_readme)
        self.reset_settings_button = self.create_button('Сбросить настройки', self.reset_settings)
        self.save_settings_button = self.create_button('Сохранить настройки', self.save_settings)
        self.start_button = self.create_button('Запуск   >>', self.start)

        self.create_layout()

    def create_button(self, name: str, func: callable) -> QPushButton:
        button = QPushButton(name)
        button.clicked.connect(func)

        return button

    def create_layout(self):
        layout = QGridLayout()
        layout.addWidget(self.readme_button, 0, 0)
        layout.addWidget(self.reset_settings_button, 1, 0)
        layout.addWidget(self.save_settings_button, 1, 1)
        layout.addWidget(self.start_button, 1, 2)

        self.setLayout(layout)

    def open_readme(self):
        print('Открыть ReadMe')

    def reset_settings(self):
        self.settings.clean_data()
        print('Сбросить настройки')

    def save_settings(self):
        print('Сохранить настройки')

    def start(self):
        print('Запуск   >>')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()

        self.set_window_parameters()
        self.main_layout = QVBoxLayout()
        self.create_main_layout()

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

        self.show()

    def set_window_parameters(self):
        self.setWindowTitle('Tag Changer')
        self.setFixedSize(QSize(800, 500))

    def create_main_layout(self):
        target_dir_widget = TargetDir(self.settings)
        artist_dirs_widget = ArtistDirs(self.settings)
        main_button_widget = MainButton(self.settings)

        self.main_layout.addWidget(target_dir_widget)
        self.main_layout.addWidget(artist_dirs_widget)
        self.main_layout.addWidget(main_button_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
