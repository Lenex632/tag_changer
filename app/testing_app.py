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
    QDialog,
    QFileDialog,
    QTextEdit,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.set_window_parameters()

        self.main_layout = QVBoxLayout()
        self.create_target_dir_layout()
        self.create_artist_dir_layout()
        self.create_main_buttons_layout()

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

        self.show()

    def set_window_parameters(self):
        self.setWindowTitle('Tag Changer')
        self.setFixedSize(QSize(800, 500))

    def create_target_dir_layout(self):
        layout = QVBoxLayout()
        label = QLabel('Укажите путь к исходной папке')
        fild = QTextEdit('Enter dir name')
        layout.addWidget(label)
        layout.addWidget(fild)
        self.main_layout.addLayout(layout)

    def create_artist_dir_layout(self):
        layout = QVBoxLayout()
        label = QLabel('Укажите папки с исполнителями для Уровня 2 (через запятую)')
        fild = QTextEdit('Enter dirs name')
        layout.addWidget(label)
        layout.addWidget(fild)
        self.main_layout.addLayout(layout)

    def create_main_buttons_layout(self):
        readme_button = QPushButton('Открыть ReadMe')
        reset_settings_button = QPushButton('Сбросить настройки')
        save_settings_button = QPushButton('Сохранить настройки')
        start_button = QPushButton('Запуск   >>')

        layout = QGridLayout()
        layout.addWidget(readme_button, 0, 0)
        layout.addWidget(reset_settings_button, 1, 0)
        layout.addWidget(save_settings_button, 1, 1)
        layout.addWidget(start_button, 1, 2)

        self.main_layout.addLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
