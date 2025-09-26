import logging
from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QInputDialog,
    QFileDialog,
    QTextEdit,
    QCheckBox,
    QTreeWidgetItem,
    QTreeWidget,
    QComboBox,
)

from settings import Settings
from db import DBController


class Directories(Enum):
    target_dir = 'Укажите путь к исходной папке'
    sync1_dir = 'Укажите путь к первой папке для синхронизации'
    sync2_dir = 'Укажите путь ко второй папке для синхронизации'
    from_dir = 'Укажите путь к папке, из которой хотите забрать новые файлы'
    to_dir = 'Укажите путь к папке, в которую хотите переместить новые файлы'


class DirWidget(QWidget):
    def __init__(self, settings: Settings, directory: Directories):
        """Класс для работы с полем для ввода target_dir"""
        super().__init__()
        self.settings = settings
        self.dir = directory

        self.label = QLabel(self.dir.value)
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
        dialog.setWindowTitle(self.dir.value)
        chosen_dir = dialog.getExistingDirectory() or self.fild.toPlainText()
        self.fild.setText(chosen_dir)

    def create_fild(self) -> QTextEdit:
        """Создаёт поле в которое будет записываться значение target_dir"""
        fild = QTextEdit()
        fild.setPlaceholderText(self.dir.value)
        if self.settings.__getattribute__(self.dir.name):
            fild.setText(self.settings.__getattribute__(self.dir.name))

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


class ArtistDirsWidget(QWidget):
    def __init__(self, settings: Settings):
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


class MainButtons(QWidget):
    def __init__(self, is_sync_tab: bool = False):
        """Класс для работы с кнопками в главном окне"""
        super().__init__()
        self.is_sync_tab = is_sync_tab
        self.db_update_checkbox = QCheckBox('Обновить базу данных основываясь на обработанных данных')
        self.readme_button = QPushButton('Открыть ReadMe')
        self.reset_settings_button = QPushButton('Сбросить настройки')
        self.save_settings_button = QPushButton('Сохранить настройки')
        self.start_button = QPushButton('Запуск   >>')

        self.create_layout()

    def create_layout(self):
        """Создаёт виджет для размещения в окне"""
        layout = QGridLayout()
        if not self.is_sync_tab:
            layout.addWidget(self.db_update_checkbox, 0, 0, 1, 2)
        layout.addWidget(self.readme_button, 1, 0)
        layout.addWidget(self.reset_settings_button, 2, 0)
        layout.addWidget(self.save_settings_button, 2, 1)
        layout.addWidget(self.start_button, 2, 2)

        self.setLayout(layout)


class FindDuplicatesButtons(QWidget):
    def __init__(self):
        """Класс для работы с кнопками в окне поиска дубликатов"""
        super().__init__()
        self.readme_button = QPushButton('Открыть ReadMe')
        self.start_button = QPushButton('Запуск   >>')

        self.create_layout()

    def create_layout(self):
        """Создаёт виджет для размещения в окне"""
        layout = QVBoxLayout()
        layout.addWidget(self.readme_button)
        layout.addWidget(self.start_button)

        self.setLayout(layout)


class FindDuplicatesResults(QWidget):
    def __init__(self, duplicates):
        """Класс для работы с результатами поиска дубликатов"""
        super().__init__()
        self.duplicates = duplicates
        self.duplicate_tree = QTreeWidget()
        self.ok_button = QPushButton('Применить')
        self.cansel_button = QPushButton('Отмена')

        self.create_layout()

    def create_layout(self):
        """Создаёт виджет для размещения в окне"""
        layout = QVBoxLayout()

        self.duplicate_tree.setHeaderHidden(True)
        for title, artist, group in self.duplicates:
            parent = QTreeWidgetItem(self.duplicate_tree)
            parent.setText(0, f'{title} - {artist}')
            parent.setCheckState(0, Qt.CheckState.Unchecked)
            parent.setFlags(parent.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
            for s in group:
                idx, file_path, *_ = s
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                child.setText(0, file_path)
                child.setCheckState(0, Qt.CheckState.Unchecked)
                child.setData(0, Qt.ItemDataRole.UserRole, idx)
        self.duplicate_tree.expandAll()
        layout.addWidget(self.duplicate_tree)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cansel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_items_for_delete(self):
        items = []

        for top_idx in range(self.duplicate_tree.topLevelItemCount()):
            parent = self.duplicate_tree.topLevelItem(top_idx)
            for idx in range(parent.childCount()):
                child = parent.child(idx)
                if child.checkState(0) is Qt.CheckState.Checked:
                    items.append((child.data(0, Qt.ItemDataRole.UserRole), child.text(0)))

        return items


class ExpansionButtons(QWidget):
    def __init__(self):
        super().__init__()

        self.readme_button = QPushButton('Открыть ReadMe')
        self.start_button = QPushButton('Запуск   >>')

        self.create_layout()

    def create_layout(self):
        """Создаёт виджет для размещения в окне"""
        layout = QHBoxLayout()
        layout.addWidget(self.readme_button)
        layout.addWidget(self.start_button)

        self.setLayout(layout)


class LibrariesWidget(QWidget):
    def __init__(self, settings: Settings, db: DBController):
        super().__init__()

        self.settings = settings
        self.db = db
        self.libraries_list = QComboBox()
        self.add_library_button = QPushButton('+')
        self.remove_library_button = QPushButton('-')

        self.create_layout()

    def create_layout(self):
        layout = QGridLayout()
        layout.addWidget(QLabel('Выберите библиотеку, либо создайте её'), 0, 0, 1, 2)
        layout.addWidget(self.libraries_list, 1, 0, 1, 2)
        layout.addWidget(self.add_library_button, 1, 3)
        layout.addWidget(self.remove_library_button, 1, 4)

        self.reload_libraries_list()
        self.add_library_button.clicked.connect(self.open_create_library_dialog)
        self.remove_library_button.clicked.connect(self.open_remove_library_dialog)

        self.setLayout(layout)

    def reload_libraries_list(self):
        self.libraries_list.clear()
        with self.db:
            libraries_list = self.db.get_tables_list()
        self.libraries_list.addItem('')
        self.libraries_list.addItems(libraries_list)
        self.libraries_list.setCurrentText(self.settings.current_library)

    def open_create_library_dialog(self):
        dlg = QInputDialog(self)
        dlg.setWindowTitle('Введите название новой библиотеки')

        if dlg.exec():
            library = dlg.textValue()
            with self.db:
                if library and library not in self.db.get_tables_list():
                    self.libraries_list.addItem(library)
                    self.db.create_table_if_not_exist(library)

    def open_remove_library_dialog(self):
        dlg = QInputDialog(self)
        dlg.setWindowTitle('Выберите, какую библиотеку хотите удалить')
        items = {}
        for idx in range(1, self.libraries_list.count()):
            items[self.libraries_list.itemText(idx)] = idx
        dlg.setComboBoxItems(items.keys())

        if dlg.exec():
            library = dlg.textValue()
            if library:
                self.libraries_list.removeItem(items[library])
                with self.db:
                    self.db.drop_table(library)


class SyncLibrariesWidget(QWidget):
    def __init__(self, settings: Settings, db: DBController):
        self.logger = logging.getLogger('App')
        super().__init__()

        self.settings = settings
        self.db = db
        self.sync1_library_list = QComboBox()
        self.sync2_library_list = QComboBox()

        self.create_layout()

    def create_layout(self):
        layout = QGridLayout()
        layout.addWidget(QLabel('Выберите библиотеки для синхронизации'), 0, 0)
        layout.addWidget(QLabel('Библиотека 1'), 1, 0)
        layout.addWidget(self.sync1_library_list, 1, 2)
        layout.addWidget(QLabel('Библиотека 2'), 2, 0)
        layout.addWidget(self.sync2_library_list, 2, 2)

        self.reload_libraries_lists()

        self.setLayout(layout)

    def reload_libraries_lists(self):
        with self.db:
            libraries_list = self.db.get_tables_list()

        self.sync1_library_list.clear()
        self.sync1_library_list.addItem('')
        self.sync1_library_list.addItems(libraries_list)

        self.sync2_library_list.clear()
        self.sync2_library_list.addItem('')
        self.sync2_library_list.addItems(libraries_list)


class SyncResult(QWidget):
    def __init__(self, differance):
        super().__init__()

        self.main_tree = QTreeWidget()
        self.difference_list = differance

        self.create_layout()

    def create_layout(self):
        layout = QVBoxLayout()

        layout.addWidget(self.main_tree)
        self.setLayout(layout)


class DialogButtons(QWidget):
    def __init__(self):
        super().__init__()

        self.ok_button = QPushButton('Применить')
        self.cansel_button = QPushButton('Отменить')

        self.create_layout()

    def create_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cansel_button)

        self.setLayout(layout)

