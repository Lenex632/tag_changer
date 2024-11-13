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
#       Next:
#               "Синхронизация"
#               В тестах добавить строчки для восстановления тестовых файлов (скорее всего нужно будет сделать через
#                   threading):
#                       rm -f test_from_dir/, test_to_dir/, test_target_dir
#                       git restore test_from_dir/, test_to_dir/, test_target_dir
# TODO остались в: tag_changer.py, db_controller.py
class MainWindow(QMainWindow):
    def __init__(self):
        """Класс главного окна"""
        super().__init__()

        self.logger = logging.getLogger('App')
        self.settings = Settings()
        self.db = DBController()

        self.main_tab = MainTab(self.settings, self.db)
        self.expansion_tab = ExpansionTab(self.settings, self.db)
        self.find_duplicates_tab = FindDuplicatesTab(self.settings, self.db)

        self.set_window_parameters()

    def set_window_parameters(self):
        """Настройка параметров окна"""
        self.setWindowTitle('Tag Changer')
        self.setFixedSize(QSize(800, 500))
        self.set_up_libraries_widget()

        # Создание и размещение вкладок
        tabs = QTabWidget()
        tabs.addTab(self.main_tab, 'Изменение тегов')
        tabs.addTab(self.expansion_tab, 'Добавление')
        tabs.addTab(self.find_duplicates_tab, 'Поиск дубликатов')
        tabs.addTab(QWidget(), 'Синхронизация')

        self.setCentralWidget(tabs)

        self.show()

    def set_up_libraries_widget(self):
        self.main_tab.libraries_widget.add_library_button.clicked.connect(self.reload_all_libraries_list)
        self.main_tab.libraries_widget.remove_library_button.clicked.connect(self.reload_all_libraries_list)

        self.expansion_tab.libraries_widget.add_library_button.clicked.connect(self.reload_all_libraries_list)
        self.expansion_tab.libraries_widget.remove_library_button.clicked.connect(self.reload_all_libraries_list)

        self.find_duplicates_tab.libraries_widget.add_library_button.clicked.connect(self.reload_all_libraries_list)
        self.find_duplicates_tab.libraries_widget.remove_library_button.clicked.connect(self.reload_all_libraries_list)

    def reload_all_libraries_list(self):
        self.main_tab.libraries_widget.reload_libraries_list()
        self.expansion_tab.libraries_widget.reload_libraries_list()
        self.find_duplicates_tab.libraries_widget.reload_libraries_list()
        # self.sync_tab.libraries_widget.reload_libraries_list()


if __name__ == '__main__':
    from logger import set_up_logger_config
    set_up_logger_config()

    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
