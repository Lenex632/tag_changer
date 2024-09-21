import sys
import configparser

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


class TargetDir(QWidget):
    def __init__(self):
        super().__init__()
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

        return fild

    def create_layout(self) -> None:
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.button)
        bottom_layout.addWidget(self.fild)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)


class ArtistDir(QWidget):
    def __init__(self):
        super().__init__()
        self.placeholder = 'Укажите папки с исполнителями для Уровня 2 (через запятую)'

        self.label = QLabel(self.placeholder)
        self.fild = self.create_fild()

        self.create_layout()

    def create_fild(self) -> QTextEdit:
        fild = QTextEdit()
        fild.setPlaceholderText(self.placeholder)

        return fild

    def create_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.fild)

        self.setLayout(layout)


class MainButton(QWidget):
    def __init__(self):
        super().__init__()

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
        print('Сбросить настройки')

    def save_settings(self):
        print('Сохранить настройки')

    def start(self):
        print('Запуск   >>')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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
        target_dir_widget = TargetDir()
        artist_dir_widget = ArtistDir()
        main_button_widget = MainButton()

        self.main_layout.addWidget(target_dir_widget)
        self.main_layout.addWidget(artist_dir_widget)
        self.main_layout.addWidget(main_button_widget)


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # app.exec()
    config = configparser.ConfigParser()
    config.read('../settings.ini')
    print(config['settings']['target_dir'])
    print(config.get('settings', 'artist_dir').split('\n'))
