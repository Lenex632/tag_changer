from enum import Enum

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QCheckBox,
    QListWidget, QFrame, QListWidgetItem, QScrollArea, QTreeWidgetItem, QTreeWidget, QTreeWidgetItemIterator
)


class Directories(Enum):
    target_dir = 'Укажите путь к исходной папке'
    sync_dir = 'Укажите путь к папке, с которой хотите синхронизироваться'
    from_dir = 'Укажите путь к папке, из которой хотите забрать новые файлы'
    to_dir = 'Укажите путь к папке, в которую хотите переместить новые файлы'


class DirWidget(QWidget):
    def __init__(self, settings, directory: Directories):
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


class MainButtons(QWidget):
    def __init__(self):
        """Класс для работы с кнопками в главном окне"""
        super().__init__()
        self.db_update_checkbox = QCheckBox('Обновить базу данных основываясь на обработанных данных')
        self.readme_button = QPushButton('Открыть ReadMe')
        self.reset_settings_button = QPushButton('Сбросить настройки')
        self.save_settings_button = QPushButton('Сохранить настройки')
        self.start_button = QPushButton('Запуск   >>')

        self.create_layout()

    def create_layout(self):
        """Создаёт виджет для размещения в окне"""
        layout = QGridLayout()
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
    def __init__(self, target_dir, duplicates):
        """Класс для работы с результатами поиска дубликатов"""
        super().__init__()
        self.duplicates_list = QListWidget()
        self.duplicates = duplicates

        for title, artist, group in duplicates:
            for s in group:
                idx, file_path, *_ = s
                self.duplicates_list.addItem(file_path)

        self.create_layout()

    def create_layout(self):
        """Создаёт виджет для размещения в окне"""
        layout = QVBoxLayout()
        test = QTreeWidget()
        test.setHeaderHidden(True)
        items = []

        for title, artist, group in self.duplicates:
            item = QTreeWidgetItem()
            item.setText(0, f'{title} - {artist}')
            for s in group:
                idx, file_path, *_ = s
                i = QTreeWidgetItem()
                i.setText(0, file_path)
                item.addChild(i)
            items.append(item)
        test.addTopLevelItems(items)
        test.expandAll()
        layout.addWidget(test)

        self.setLayout(layout)
