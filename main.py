import logging
import sys
import time

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QInputDialog,
    QFileDialog,
    QDialogButtonBox,
    QLineEdit,
    QTreeWidgetItem,
    QProgressBar
)

from db import DBController
from config import AppConfig
from tag_changer import TagChanger

from ui import Ui_MainWindow, Ui_DuplicatesDlg, Ui_SyncDlg

# TODO:
#   перенести все todo, настройки и прочее с прошлого файла
#   пререписать README, тестики, скриншоты и тд.
#   подключить бд
#   посмотреть, можно ли работу с кастомными функциями привязать в QtCreator, что бы тут не захламлять код
#   перенести всё с old
#   ...

dup = [
    ["name 1", "artist", ["path 1", "path 2"]],
    ["name 2", "artist", ["path 1", "path 2", "path 3", "path 4"]],
    ["name 3", "artist", ["path 1", "path 2", "path 3"]],
    ["name 4", "artist", ["path 1", "path 2"]]
]
sync_1 = [
    ["artist1", "name1", "path1"],
    ["artist2", "name2", "path2"],
    ["artist3", "name3", "path3"],
]
sync_2 = [
    ["artist11", "name11", "path11"],
    ["artist12", "name12", "path12"],
    ["artist13", "name13", "path13"],
    ["artist14", "name14", "path14"],
    [
        "super duper big artisn name with extra chease",
        "some name that contains a lot of letters and big coke",
        "path/so/far/away/that/even/you/mam/cant/find/your/large/soda/"
    ]
]
libs = ['main', 'duplicates', 'sync1', 'sync2']


def toggle_check_state(tree_item: QTreeWidgetItem):
    if tree_item.checkState(0) is Qt.CheckState.Checked:
        tree_item.setCheckState(0, Qt.CheckState.Unchecked)
    else:
        tree_item.setCheckState(0, Qt.CheckState.Checked)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__()
        self.ui = Ui_MainWindow()
        self.config = AppConfig()
        self.db = DBController()
        self.tag_changer = TagChanger()

        self.ui.setupUi(self)
        self.ui.statusBar.setContentsMargins(10, 2, 10, 5)
        self.update_libraries()
        self.update_main_settings()
        self.update_add_settings()
        self.update_duplicate_settings()
        self.update_sync_settings()

        self.ui.start_button.clicked.connect(self.start_main)
        self.ui.save_button.clicked.connect(self.save_main_settings)
        self.ui.save_button.clicked.connect(lambda: self.show_message('Настройки сохранены'))
        self.ui.reset_button.clicked.connect(self.reset_main_settings)
        self.ui.reset_button.clicked.connect(lambda: self.show_message('Настройки сброшены'))
        self.ui.target_dir_button.clicked.connect(lambda: self.choose_dir(self.ui.target_dir_field))
        self.ui.add_lib_button.clicked.connect(self.add_lib)
        self.ui.remove_lib_button.clicked.connect(self.remove_lib)

        self.ui.start_button_2.clicked.connect(lambda: self.show_message('some 2'))
        self.ui.save_button_2.clicked.connect(self.save_add_settings)
        self.ui.save_button_2.clicked.connect(lambda: self.show_message('Настройки сохранены'))
        self.ui.reset_button_2.clicked.connect(self.reset_add_settings)
        self.ui.reset_button_2.clicked.connect(lambda: self.show_message('Настройки сброшены'))
        self.ui.from_dir_button.clicked.connect(lambda: self.choose_dir(self.ui.from_dir_field))
        self.ui.to_dir_button.clicked.connect(lambda: self.choose_dir(self.ui.to_dir_field))

        self.ui.start_button_3.clicked.connect(self.start_duplicates)
        self.ui.save_button_3.clicked.connect(self.save_duplicate_settings)
        self.ui.save_button_3.clicked.connect(lambda: self.show_message('Настройки сохранены'))
        self.ui.reset_button_3.clicked.connect(self.reset_duplicate_settings)
        self.ui.reset_button_3.clicked.connect(lambda: self.show_message('Настройки сброшены'))
        self.ui.target_dir_button_3.clicked.connect(lambda: self.choose_dir(self.ui.duplicates_dir_field))

        self.ui.start_button_4.clicked.connect(self.start_sync)
        self.ui.save_button_4.clicked.connect(self.save_sync_settings)
        self.ui.save_button_4.clicked.connect(lambda: self.show_message('Настройки сохранены'))
        self.ui.reset_button_4.clicked.connect(self.reset_sync_settings)
        self.ui.reset_button_4.clicked.connect(lambda: self.show_message('Настройки сброшены'))
        self.ui.sync_dir_button_1.clicked.connect(lambda: self.choose_dir(self.ui.sync_dir_field_1))
        self.ui.sync_dir_button_2.clicked.connect(lambda: self.choose_dir(self.ui.sync_dir_field_2))

    def start_main(self) -> None:
        """Запуск скрипта"""

        self.ui.statusBar.showMessage('Скрипт начал работу')

        target_dir = Path(self.ui.target_dir_field.text())
        artist_dirs = self.ui.artist_dir_field.toPlainText().split('\n')
        library = self.ui.library_field.currentText()
        db_update = True if self.ui.update_lib_checkbox.checkState() is Qt.CheckState.Checked else False

        if not target_dir or (not library and db_update):
            self.show_message('Не все данные были заполнены')
            self.logger.info('Не все данные были заполнены')
            return 1

        self.tag_changer.set_up_target_dir(target_dir)
        self.tag_changer.set_up_artist_dirs(artist_dirs)

        # TODO: понять, что сделать с прогресс баром. зарание считать сколько песен обрабатывается достаточно сложно
        # progress_bar = QProgressBar()
        # progress_bar.setRange(0, 100)
        # self.ui.statusBar.addPermanentWidget(progress_bar)
        # progress_bar.show()
        # progress_bar.setValue(i * 10 + 10)
        # self.ui.statusBar.removeWidget(progress_bar)

        items = self.tag_changer.start(target_dir)
        for i, song_data in enumerate(items):
            self.logger.debug(f'{song_data.artist} - {song_data.title}')

        self.logger.info('Запуск скрипта')
        items = self.tag_changer.start(target_dir)
        if db_update:
            with self.db:
                self.db.clear_table(library)
                for song_data in items:
                    self.db.insert(song_data, library)
        else:
            for song_data in items:
                self.logger.debug(f'{song_data.artist} - {song_data.title}')

        self.show_message('Скрипт завершил работу')
        self.logger.info('Скрипт завершил работу')

    def start_duplicates(self) -> None:
        # TODO: тут заводим функцию поиска дубликатов по бд, потом пхаем результат в класс.
        dlg = DuplicatesDlg(duplicates=dup, parent=self)
        dlg.exec()

    def start_sync(self) -> None:
        dlg = SyncDlg(sync_elements_1=sync_1, sync_elements_2=sync_2, parent=self)
        dlg.exec()

    def show_message(self, message: str) -> None:
        self.ui.statusBar.showMessage(message, 4000)

    def choose_dir(self, fild: QLineEdit) -> None:
        dlg = QFileDialog(parent=self)
        dlg.setWindowTitle('Выберите папку')
        fild.setText(dlg.getExistingDirectory() or fild.text())

    def update_libraries(self) -> None:
        self.ui.library_field.clear()
        self.ui.add_lib_field.clear()
        self.ui.duplicates_lib_field.clear()
        self.ui.sync_lib_field_1.clear()
        self.ui.sync_lib_field_2.clear()

        self.ui.library_field.addItems(libs)
        self.ui.add_lib_field.addItems(libs)
        self.ui.duplicates_lib_field.addItems(libs)
        self.ui.sync_lib_field_1.addItems(libs)
        self.ui.sync_lib_field_2.addItems(libs)

        self.ui.library_field.setCurrentText(self.config.library)
        self.ui.add_lib_field.setCurrentText(self.config.add_lib)
        self.ui.duplicates_lib_field.setCurrentText(self.config.duplicates_lib)
        self.ui.sync_lib_field_1.setCurrentText(self.config.sync_lib_1)
        self.ui.sync_lib_field_2.setCurrentText(self.config.sync_lib_2)

    def add_lib(self) -> None:
        add_lib_dlg = QInputDialog(self)
        add_lib_dlg.setWindowTitle('Введите название новой библиотеки')

        if add_lib_dlg.exec():
            lib = add_lib_dlg.textValue()
            libs.append(lib)
            self.update_libraries()

    def remove_lib(self) -> None:
        remove_lib_dlg = QInputDialog(self)
        remove_lib_dlg.setWindowTitle('Выберите, какую библиотеку хотите удалить')
        remove_lib_dlg.setComboBoxItems(libs)

        if remove_lib_dlg.exec():
            lib = remove_lib_dlg.textValue()
            if lib:
                libs.remove(lib)
            self.update_libraries()

    def update_main_settings(self) -> None:
        self.ui.target_dir_field.setText(self.config.target_dir)
        artist_dir_value = '\n'.join(self.config.artist_dir)
        self.ui.artist_dir_field.setText(artist_dir_value)
        self.ui.library_field.setCurrentText(self.config.library)
        self.ui.update_lib_checkbox.setCheckState(
            Qt.CheckState.Checked if self.config.update_lib else Qt.CheckState.Unchecked
        )

    def save_main_settings(self) -> None:
        self.config.target_dir = self.ui.target_dir_field.text()
        self.config.artist_dir = self.ui.artist_dir_field.toPlainText().split('\n')
        self.config.library = self.ui.library_field.currentText()
        self.config.update_lib = True if self.ui.update_lib_checkbox.checkState() is Qt.CheckState.Checked else False
        self.config.update()

    def reset_main_settings(self) -> None:
        self.config.target_dir = ''
        self.config.artist_dir = ''
        self.config.library = ''
        self.config.update_lib = False
        self.config.update()
        self.update_main_settings()

    def update_add_settings(self) -> None:
        self.ui.to_dir_field.setText(self.config.to_dir)
        self.ui.from_dir_field.setText(self.config.from_dir)
        self.ui.add_lib_field.setCurrentText(self.config.add_lib)

    def save_add_settings(self) -> None:
        self.config.to_dir = self.ui.to_dir_field.text()
        self.config.from_dir = self.ui.from_dir_field.text()
        self.config.add_lib = self.ui.add_lib_field.currentText()
        self.config.update()

    def reset_add_settings(self) -> None:
        self.config.to_dir = ''
        self.config.from_dir = ''
        self.config.add_lib = ''
        self.config.update()
        self.update_add_settings()

    def update_duplicate_settings(self) -> None:
        self.ui.duplicates_dir_field.setText(self.config.duplicates_dir)
        self.ui.duplicates_lib_field.setCurrentText(self.config.duplicates_lib)

    def save_duplicate_settings(self) -> None:
        self.config.duplicates_dir = self.ui.duplicates_dir_field.text()
        self.config.duplicates_lib = self.ui.duplicates_lib_field.currentText()
        self.config.update()

    def reset_duplicate_settings(self) -> None:
        self.config.duplicates_dir = ''
        self.config.duplicates_lib = ''
        self.config.update()
        self.update_duplicate_settings()

    def update_sync_settings(self) -> None:
        self.ui.sync_dir_field_1.setText(self.config.sync_dir_1)
        self.ui.sync_dir_field_2.setText(self.config.sync_dir_2)
        self.ui.sync_lib_field_1.setCurrentText(self.config.sync_lib_1)
        self.ui.sync_lib_field_2.setCurrentText(self.config.sync_lib_2)

    def save_sync_settings(self) -> None:
        self.config.sync_dir_1 = self.ui.sync_dir_field_1.text()
        self.config.sync_dir_2 = self.ui.sync_dir_field_2.text()
        self.config.sync_lib_1 = self.ui.sync_lib_field_1.currentText()
        self.config.sync_lib_2 = self.ui.sync_lib_field_2.currentText()
        self.config.update()

    def reset_sync_settings(self) -> None:
        self.config.sync_dir_1 = ''
        self.config.sync_dir_2 = ''
        self.config.sync_lib_1 = ''
        self.config.sync_lib_2 = ''
        self.config.update()
        self.update_sync_settings()


class DuplicatesDlg(QDialog):
    def __init__(self, duplicates: list, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_DuplicatesDlg()
        self.ui.setupUi(self)
        self.duplicates = duplicates

        for title, artist, group in self.duplicates:
            parent = QTreeWidgetItem(self.ui.duplicates_dlg_tree)
            parent.setText(0, artist)
            parent.setText(1, title)
            parent.setCheckState(0, Qt.CheckState.Unchecked)
            parent.setFlags(parent.flags() | Qt.ItemFlag.ItemIsAutoTristate)
            for idx, file_path in enumerate(group):
                child = QTreeWidgetItem(parent)
                child.setText(0, str(idx))
                child.setText(1, file_path)
                child.setCheckState(0, Qt.CheckState.Unchecked)

        self.ui.duplicates_dlg_tree.resizeColumnToContents(0)
        self.ui.duplicates_dlg_tree.resizeColumnToContents(1)
        self.ui.duplicates_dlg_tree.itemDoubleClicked.connect(toggle_check_state)
        self.ui.duplicates_dlg_tree.expandAll()
        self.ui.duplicates_dlg_tree.sortItems(0, Qt.SortOrder.AscendingOrder)

        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.ui.buttonBox.accepted)
        self.ui.buttonBox.accepted.connect(self.accept_changes)

    def accept_changes(self) -> None:
        for i in range(self.ui.duplicates_dlg_tree.topLevelItemCount()):
            parent = self.ui.duplicates_dlg_tree.topLevelItem(i)
            for j in range(parent.childCount()):
                child = parent.child(j)
                if child.checkState(0) is Qt.CheckState.Checked:
                    artist, title = parent.text(0), parent.text(1)
                    idx, path = child.text(0), child.text(1)
                    print(artist + title + idx + path)


class SyncDlg(QDialog):
    def __init__(self, sync_elements_1: list, sync_elements_2: list, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_SyncDlg()
        self.ui.setupUi(self)
        self.sync_elements_1 = sync_elements_1
        self.sync_elements_2 = sync_elements_2

        for artist, title, file_path in self.sync_elements_1:
            element = QTreeWidgetItem(self.ui.sync_dlg_tree_1)
            element.setText(0, artist)
            element.setText(1, title)
            element.setText(2, file_path)
            element.setCheckState(0, Qt.CheckState.Unchecked)
        self.ui.sync_dlg_tree_1.resizeColumnToContents(0)
        self.ui.sync_dlg_tree_1.resizeColumnToContents(1)
        self.ui.sync_dlg_tree_1.resizeColumnToContents(2)
        self.ui.sync_dlg_tree_1.itemDoubleClicked.connect(toggle_check_state)
        self.ui.sync_dlg_tree_1.sortItems(0, Qt.SortOrder.AscendingOrder)

        for artist, title, file_path in self.sync_elements_2:
            element = QTreeWidgetItem(self.ui.sync_dlg_tree_2)
            element.setText(0, artist)
            element.setText(1, title)
            element.setText(2, file_path)
            element.setCheckState(0, Qt.CheckState.Unchecked)
        self.ui.sync_dlg_tree_2.resizeColumnToContents(0)
        self.ui.sync_dlg_tree_2.resizeColumnToContents(1)
        self.ui.sync_dlg_tree_2.resizeColumnToContents(2)
        self.ui.sync_dlg_tree_2.itemDoubleClicked.connect(toggle_check_state)
        self.ui.sync_dlg_tree_2.sortItems(0, Qt.SortOrder.AscendingOrder)

        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.ui.buttonBox.accepted)
        self.ui.buttonBox.accepted.connect(self.accept_changes)

    def accept_changes(self) -> None:
        for i in range(self.ui.sync_dlg_tree_1.topLevelItemCount()):
            item = self.ui.sync_dlg_tree_1.topLevelItem(i)
            if item.checkState(0) is Qt.CheckState.Checked:
                artist, title, path = item.text(0), item.text(1), item.text(2)
                print(artist, title, path)

        for i in range(self.ui.sync_dlg_tree_2.topLevelItemCount()):
            item = self.ui.sync_dlg_tree_2.topLevelItem(i)
            if item.checkState(0) is Qt.CheckState.Checked:
                artist, title, path = item.text(0), item.text(1), item.text(2)
                print(artist, title, path)


def main() -> None:
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    from logger import set_up_logger_config
    set_up_logger_config()

    main()

