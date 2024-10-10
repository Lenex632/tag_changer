import logging
from pathlib import Path
import sqlite3

from model import SongData, TableModel


# TODO инициализировать базу надо вручную
class DBController:
    def __init__(self, db_name: str = 'music.db', table_name: str = 'music') -> None:
        """
        Класс управления базой данных.
        Операции будут проводиться с помощью контекстного менеджера.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_name = db_name
        self.db_path = Path(Path(__file__).parent, self.db_name)
        self.table_name = table_name
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

    def create_table_if_not_exist(self) -> None:
        """Создаёт базу данных и таблицу self.table_name, если такие не существуют"""
        table_columns = f'{", ".join(f"{key} {value}" for key, value in self.table_model.items())}'
        query = f'CREATE TABLE IF NOT EXISTS {self.table_name} ({table_columns})'
        self.execute(query)

    def clear_table(self):
        """Очищение таблицы от всех данных"""
        query = f'DELETE FROM {self.table_name}'
        self.execute(query)
        self.logger.info(f'"{self.table_name}" has been cleared')

    def insert(self, song_data: SongData):
        """Вставка значений song_data в таблицу"""
        # Подготовка значений, а то sqlite3 будет ругаться
        song_data.file_path = str(song_data.file_path)
        song_data.image = str(song_data.image) if song_data.image else None
        song_data.feat = song_data.feat if song_data.feat else None
        song_data.special = song_data.special if song_data.special else None

        keys = f'{", ".join(f"{key}" for key in song_data.__dict__.keys())}'
        values = list(song_data.__dict__.values())

        query = f'INSERT INTO {self.table_name} ({keys}) VALUES ({", ".join("?" for _ in values)})'
        self.execute(query, params=values)

        self.logger.debug(f'"{song_data.artist} - {song_data.title}" has been added to table "{self.table_name}"')

    def delete(self, song_id: int):
        """Удаление элемента по id"""
        query = f'DELETE FROM {self.table_name} WHERE song_id={song_id}'
        self.execute(query)
        self.logger.debug(f'Song with id={song_id} has been deleted from table "{self.table_name}"')

    def find(self, condition: str = None) -> list:
        """
        Нахождение элементов по condition (в формате 'song_id = 1'), либо вообще всей таблички, если condition=None
        """
        if condition:
            query = f'SELECT * FROM {self.table_name} WHERE {condition}'
        else:
            query = f'SELECT * FROM {self.table_name}'
        results = self.execute_and_fetch(query)
        self.logger.info(f'{len(results)} rows was found in table "{self.table_name}" for {condition=}')

        return results

    def update(self, condition: str, new: str):
        """
        Нахождение элемента с condition (в формате 'song_id = 1') и обновление его
        параметров new (в формате 'title = "New Title"')
        """
        query = f'UPDATE {self.table_name} SET {new} WHERE {condition}'
        self.logger.debug(f'Update table "{self.table_name}" where {condition} with new parameters {new}')
        self.execute(query)

    def find_duplicates(self):
        query = f'''
            SELECT title, artist, COUNT(*)
            FROM {self.table_name}
            GROUP BY artist, title
            HAVING COUNT(*) > 1;
        '''
        results = self.execute_and_fetch(query)
        self.logger.info(f'{len(results)} duplicates was found in table "{self.table_name}"')

        duplicates = []
        for res in results:
            condition = f'title = "{res[0]}" AND artist = "{res[1]}"'
            duplicate = self.find(condition)
            duplicates.append(duplicate)

        return duplicates


if __name__ == '__main__':
    from logger import set_up_logger_config
    set_up_logger_config()

    db = DBController()
