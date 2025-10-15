import shutil
import logging
import sys

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
    # QProgressBar
)

from db import DBController
from config import AppConfig
from model import SongData
from tag_changer import TagChanger

from ui import Ui_MainWindow, Ui_DuplicatesDlg, Ui_SyncDlg

# TODO:
#   ПОЛЮБОМУ сделать многопроцессорность! Слишком долго для 4к треков!
#   Next:
#       Пререписать README, тестики, скриншоты и тд.
#       Прогрессбар
#       Сделать artist_dir нормальным списком
#           + что бы кирилица не шифровалась в абракадабру
#       В python 3.14 появильсь t-строки их можно попробовать поюзать в БД
#           что бы не было проблем с иньекциями


def toggle_check_state(tree_item: QTreeWidgetItem):
    if tree_item.checkState(0) is Qt.CheckState.Checked:
        tree_item.setCheckState(0, Qt.CheckState.Unchecked)
    else:
        tree_item.setCheckState(0, Qt.CheckState.Checked)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        self.logger = logging.getLogger('Main')
        super().__init__()
        self.ui = Ui_MainWindow()
        self.config = AppConfig()
        self.db = DBController()
        self.tag_changer = TagChanger()
        with self.db as db:
            self.libs = db.get_tables_list()

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

        self.ui.start_button_2.clicked.connect(self.start_add)
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
        self.tag_changer.target_dir = target_dir
        self.tag_changer.artist_dirs = artist_dirs

        # TODO: Понять, что сделать с прогресс баром.
        #       Зарание считать сколько песен обрабатывается достаточно сложно
        # progress_bar = QProgressBar()
        # progress_bar.setRange(0, 100)
        # self.ui.statusBar.addPermanentWidget(progress_bar)
        # progress_bar.show()
        # progress_bar.setValue(i * 10 + 10)
        # self.ui.statusBar.removeWidget(progress_bar)

        self.logger.info('Запуск скрипта')
        items = self.tag_changer.start(target_dir)
        if db_update:
            with self.db:
                self.db.drop_table(library)
                self.db.create_table_if_not_exist(library)
            for song_data in items:
                with self.db:
                    self.db.insert(library, song_data)
        else:
            for song_data in items:
                pass
        self.tag_changer.delete_images(target_dir)

        self.show_message('Скрипт завершил работу')
        self.logger.info('Скрипт завершил работу')

    def start_add(self) -> None:
        self.ui.statusBar.showMessage('Скрипт начал работу')
        from_dir = Path(self.ui.from_dir_field.text())
        to_dir = Path(self.ui.to_dir_field.text())
        library = self.ui.add_lib_field.currentText()
        artist_dirs = self.ui.artist_dir_field.toPlainText().split('\n')
        self.tag_changer.target_dir = from_dir
        self.tag_changer.artist_dirs = artist_dirs

        self.logger.info('Запуск скрипта')
        items = self.tag_changer.start(from_dir)
        for song_data in items:
            with self.db:
                self.db.insert(library, song_data)
            path_1 = Path(from_dir, song_data.file_path)
            path_2 = Path(to_dir, song_data.file_path)
            path_2.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(path_1, path_2, shutil.copyfile)
        self.tag_changer.delete_images(from_dir)
        self.show_message('Скрипт завершил работу')
        self.logger.info('Скрипт завершил работу')

    def start_duplicates(self) -> None:
        # TODO: выводить какие-то сообщения с результатом работы
        directory = self.ui.duplicates_dir_field.text()
        library = self.ui.duplicates_lib_field.currentText()
        with self.db:
            duplicates = self.db.find_duplicates(table=library)
        dlg = DuplicatesDlg(duplicates=duplicates, parent=self)
        dlg.exec()

        self.remove_elements(elements=dlg.results, directory=directory, library=library)

    def start_sync(self) -> None:
        # TODO: выводить какие-то сообщения с результатом работы
        target_dir_1 = self.ui.sync_dir_field_1.text()
        lib_1 = self.ui.sync_lib_field_1.currentText()
        target_dir_2 = self.ui.sync_dir_field_2.text()
        lib_2 = self.ui.sync_lib_field_2.currentText()
        with self.db:
            sync_elements_1, sync_elements_2 = self.db.find_differences(lib_1, lib_2)
        dlg = SyncDlg(sync_elements_1, sync_elements_2, parent=self)
        dlg.exec()

        self.remove_elements(elements=dlg.to_delete_1, directory=target_dir_1, library=lib_1)
        self.remove_elements(elements=dlg.to_delete_2, directory=target_dir_2, library=lib_2)
        self.copy_elements(
            elements=dlg.to_sync_1,
            dir_1=target_dir_1,
            dir_2=target_dir_2,
            lib_1=lib_1,
            lib_2=lib_2
        )
        self.copy_elements(
            elements=dlg.to_sync_2,
            dir_1=target_dir_2,
            dir_2=target_dir_1,
            lib_1=lib_2,
            lib_2=lib_1
        )

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

        self.ui.library_field.addItems(self.libs)
        self.ui.add_lib_field.addItems(self.libs)
        self.ui.duplicates_lib_field.addItems(self.libs)
        self.ui.sync_lib_field_1.addItems(self.libs)
        self.ui.sync_lib_field_2.addItems(self.libs)

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
            with self.db:
                self.db.create_table_if_not_exist(lib)
            self.libs.append(lib)
            self.update_libraries()

    def remove_lib(self) -> None:
        remove_lib_dlg = QInputDialog(self)
        remove_lib_dlg.setWindowTitle('Выберите, какую библиотеку хотите удалить')
        remove_lib_dlg.setComboBoxItems(self.libs)

        if remove_lib_dlg.exec():
            lib = remove_lib_dlg.textValue()
            if lib:
                self.libs.remove(lib)
                with self.db:
                    self.db.drop_table(lib)
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

    def remove_elements(self, elements: tuple[int, str | Path], directory: str | Path, library: str) -> None:
        self.logger.debug(elements)
        if elements:
            for song_id, file_path in elements:
                full_path = Path(directory, file_path)
                with self.db:
                    self.db.delete(table=library, song_id=song_id)
                    try:
                        full_path.unlink()
                    except FileNotFoundError:
                        # TODO: добавить какой-нибудь диалог,
                        #   что вот это вот не получилось, поэтому и в бд не получилось
                        #   НО при этом надо что-то делать с уже удалёнными файлами
                        #   либо просить заново отсканировать... либо ещё чего...
                        self.logger.error('Не удалось удалить файл. Изменения в бд отмененны')
                        raise

    def copy_elements(
        self,
        elements: tuple[int, str | Path],
        dir_1: str | Path,
        dir_2: str | Path,
        lib_1: str,
        lib_2: str
    ) -> None:
        for song_id, file_path in elements:
            full_path_1 = Path(dir_1, file_path)
            full_path_2 = Path(dir_2, file_path)
            self.logger.debug(f'{full_path_1} -> {full_path_2}')
            with self.db:
                db_data = SongData(*self.db.find(lib_1, f"song_id = '{song_id}'")[1:])
                self.db.insert(lib_2, db_data)
            full_path_2.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(full_path_1, full_path_2)


class DuplicatesDlg(QDialog):
    def __init__(self, duplicates: list, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_DuplicatesDlg()
        self.ui.setupUi(self)
        self.duplicates = duplicates
        self.results = []

        for title, artist, group in self.duplicates:
            parent = QTreeWidgetItem(self.ui.duplicates_dlg_tree)
            parent.setText(0, artist)
            parent.setText(1, title)
            parent.setCheckState(0, Qt.CheckState.Unchecked)
            parent.setFlags(parent.flags() | Qt.ItemFlag.ItemIsAutoTristate)
            for element in group:
                song_id = element[0]
                file_path = element[1]
                child = QTreeWidgetItem(parent)
                child.setText(0, str(song_id))
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
                    song_id, file_path = child.text(0), child.text(1)
                    # artist, title = parent.text(0), parent.text(1)
                    # print(f'{artist} + {title} + {song_id} + {file_path}')
                    self.results.append((song_id, file_path))


class SyncDlg(QDialog):
    def __init__(self, sync_elements_1: list, sync_elements_2: list, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_SyncDlg()
        self.ui.setupUi(self)
        self.sync_elements_1 = sync_elements_1
        self.sync_elements_2 = sync_elements_2
        self.to_delete_1 = []
        self.to_delete_2 = []
        self.to_sync_1 = []
        self.to_sync_2 = []

        for song_id, file_path, title, artist, *_ in self.sync_elements_1:
            element = QTreeWidgetItem(self.ui.sync_dlg_tree_1)
            element.setText(0, str(song_id))
            element.setText(1, artist)
            element.setText(2, title)
            element.setText(3, file_path)
            element.setCheckState(0, Qt.CheckState.Checked)
        self.ui.sync_dlg_tree_1.resizeColumnToContents(0)
        self.ui.sync_dlg_tree_1.resizeColumnToContents(1)
        self.ui.sync_dlg_tree_1.resizeColumnToContents(2)
        self.ui.sync_dlg_tree_1.resizeColumnToContents(3)
        self.ui.sync_dlg_tree_1.itemDoubleClicked.connect(toggle_check_state)
        self.ui.sync_dlg_tree_1.sortItems(0, Qt.SortOrder.AscendingOrder)

        for song_id, file_path, title, artist, *_ in self.sync_elements_2:
            element = QTreeWidgetItem(self.ui.sync_dlg_tree_2)
            element.setText(0, str(song_id))
            element.setText(1, artist)
            element.setText(2, title)
            element.setText(3, file_path)
            element.setCheckState(0, Qt.CheckState.Checked)
        self.ui.sync_dlg_tree_2.resizeColumnToContents(0)
        self.ui.sync_dlg_tree_2.resizeColumnToContents(1)
        self.ui.sync_dlg_tree_2.resizeColumnToContents(2)
        self.ui.sync_dlg_tree_2.resizeColumnToContents(3)
        self.ui.sync_dlg_tree_2.itemDoubleClicked.connect(toggle_check_state)
        self.ui.sync_dlg_tree_2.sortItems(0, Qt.SortOrder.AscendingOrder)

        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.ui.buttonBox.accepted)
        self.ui.buttonBox.accepted.connect(self.accept_changes)

    def accept_changes(self) -> None:
        for i in range(self.ui.sync_dlg_tree_1.topLevelItemCount()):
            item = self.ui.sync_dlg_tree_1.topLevelItem(i)
            song_id, file_path = item.text(0), item.text(3)
            if item.checkState(0) is Qt.CheckState.Unchecked:
                self.to_delete_1.append((song_id, file_path))
            else:
                self.to_sync_1.append((song_id, file_path))

        for i in range(self.ui.sync_dlg_tree_2.topLevelItemCount()):
            item = self.ui.sync_dlg_tree_2.topLevelItem(i)
            song_id, file_path = item.text(0), item.text(3)
            if item.checkState(0) is Qt.CheckState.Unchecked:
                self.to_delete_2.append((song_id, file_path))
            else:
                self.to_sync_2.append((song_id, file_path))


def main() -> None:
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    from logger import set_up_logger_config
    set_up_logger_config()

    main()

