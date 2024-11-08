import logging
from pathlib import Path
import sqlite3

from model import SongData, TableModel


# TODO инициализировать базу надо вручную
class DBController:
    def __init__(self, db_name: str = 'music.db') -> None:
        """
        Класс управления базой данных.
        Операции будут проводиться с помощью контекстного менеджера.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_name = db_name
        self.db_path = Path(Path(__file__).parent, self.db_name)
        self.main_table = 'main'
        self.sync_table = 'sync'
        self.table_model = TableModel().__dict__

    def __enter__(self) -> "DBController":
        self.connection = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.logger.error(f'Cant commit changes to db "{self.db_name}"')
                self.connection.rollback()
            self.connection.close()

    def execute(self, query: str, params: tuple | list | None = None) -> None:
        """Выполняет запрос query, ничего не возвращает"""
        cursor = self.connection.cursor()
        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        cursor.close()

    def execute_and_fetch(self, query: str):
        """Выполняет запрос query, возвращает полученные в его результате значения"""
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result

    def create_table_if_not_exist(self, table: str = 'main') -> None:
        """Создаёт базу данных и таблицу table, если такие не существуют"""
        table_columns = f'{", ".join(f"{key} {value}" for key, value in self.table_model.items())}'
        query = f'CREATE TABLE IF NOT EXISTS {table} ({table_columns})'
        self.execute(query)

    def get_tables_list(self) -> list | tuple:
        query = 'SELECT name FROM sqlite_master WHERE type="table" AND name NOT LIKE "sqlite_%"'
        result = self.execute_and_fetch(query)
        result = list(map(lambda x: x[0], result))

        return result

    def clear_table(self) -> None:
        """Очищение таблицы от всех данных"""
        query = f'DELETE FROM {self.main_table}'
        self.execute(query)
        self.logger.info(f'"{self.main_table}" has been cleared')

    def drop_table(self, table) -> None:
        """Удаляет выбранную таблицу"""
        query = f'DROP TABLE {table}'
        self.execute(query)
        self.logger.info(f'"{table}" has been deleted')

    def insert(self, song_data: SongData) -> None:
        """Вставка значений song_data в таблицу"""
        # Подготовка значений, а то sqlite3 будет ругаться
        song_data.file_path = str(song_data.file_path)
        song_data.image = str(song_data.image) if song_data.image else None
        song_data.feat = song_data.feat if song_data.feat else None
        song_data.special = song_data.special if song_data.special else None

        keys = f'{", ".join(f"{key}" for key in song_data.__dict__.keys())}'
        values = list(song_data.__dict__.values())

        query = f'INSERT INTO {self.main_table} ({keys}) VALUES ({", ".join("?" for _ in values)})'
        self.execute(query, params=values)

        self.logger.debug(f'"{song_data.artist} - {song_data.title}" has been added to table "{self.main_table}"')

    def delete(self, song_id: int) -> None:
        """Удаление элемента по id"""
        query = f'DELETE FROM {self.main_table} WHERE song_id={song_id}'
        self.execute(query)
        self.logger.debug(f'Song with id={song_id} has been deleted from table "{self.main_table}"')

    def find(self, condition: str = None) -> list:
        """
        Нахождение элементов по condition (в формате 'song_id = 1'), либо вообще всей таблички, если condition=None
        """
        if condition:
            query = f'SELECT * FROM {self.main_table} WHERE {condition}'
        else:
            query = f'SELECT * FROM {self.main_table}'
        results = self.execute_and_fetch(query)
        self.logger.info(f'{len(results)} rows was found in table "{self.main_table}" for {condition=}')

        return results

    def update(self, condition: str, new: str) -> None:
        """
        Нахождение элемента с condition (в формате 'song_id = 1') и обновление его
        параметров new (в формате 'title = "New Title"')
        """
        query = f'UPDATE {self.main_table} SET {new} WHERE {condition}'
        self.logger.debug(f'Update table "{self.main_table}" where {condition} with new parameters {new}')
        self.execute(query)

    def find_duplicates(self) -> list[tuple]:
        query = f'''
            SELECT title, artist, COUNT(*)
            FROM {self.main_table}
            GROUP BY artist, title
            HAVING COUNT(*) > 1;
        '''
        results = self.execute_and_fetch(query)
        self.logger.info(f'{len(results)} groups of duplicates was found in table "{self.main_table}"')

        duplicates = []
        for res in results:
            title = res[0]
            artist = res[1]
            condition = f'title = "{title}" AND artist = "{artist}"'
            duplicate = self.find(condition)
            duplicates.append((title, artist, duplicate))

        return duplicates


if __name__ == '__main__':
    from logger import set_up_logger_config
    set_up_logger_config()

    db = DBController()

    with db:
        db.create_table_if_not_exist()
        dup = db.find_duplicates()

    for t, a, g in dup:
        print(t, a)
        print(f'{"":*^20}')
        for s in g:
            idx, file_path, *_ = s
            print(file_path)
