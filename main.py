import logging
import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget

from app import MainTab, FindDuplicatesTab, ExpansionTab
from db import DBController
from settings import Settings


# TODO
#       По переписывать тестики.
#       Подкорректировать settings, возможно убрать extension.
#       Добавить в settings параметры библиотек, что бы они были общими для всех вкладок
#       Next:
#               "Синхронизация"
#               Добавить выбор библиотеки в "Поиск дубликатов"
# TODO остались в: app_tubs.py, tag_changer.py, db_controller.py
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
        tabs.addTab(MainTab(self.settings, self.db), 'Изменение тегов')
        tabs.addTab(ExpansionTab(self.settings, self.db), 'Добавление')
        tabs.addTab(FindDuplicatesTab(self.settings, self.db), 'Поиск дубликатов')
        tabs.addTab(QWidget(), 'Синхронизация')

        self.setCentralWidget(tabs)

        self.show()


if __name__ == '__main__':
    from logger import set_up_logger_config
    set_up_logger_config()

    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
