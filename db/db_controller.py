import logging
from pathlib import Path
import sqlite3

from model import SongData, TableModel


class DBController:
    def __init__(self, db_name: str = 'music.db', table_name: str = 'music') -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_name = db_name
        self.db_path = Path(Path(__file__).parent, self.db_name)
        self.table_name = table_name
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

        self.create_table_if_not_exists()
        self.logger.info(f'Database "{self.db_name}" is ready')

    def __del__(self) -> None:
        if self.connection:
            try:
                self.connection.commit()
            except Exception as e:
                self.logger.error(f'Cant commit changes to db "{self.db_name}". Error: {e}')
            finally:
                self.connection.close()

    def create_table_if_not_exists(self) -> None:
        """Создание новой таблицы и ли бд"""
        table_columns = f'{", ".join(f"{key} {value}" for key, value in TableModel().__dict__.items())}'
        query = f'CREATE TABLE IF NOT EXISTS {self.table_name} ({table_columns})'
        self.cursor.execute(query)
        self.connection.commit()

    def clear_table(self):
        """Очищение таблицы от всех данных"""
        query = f'DELETE FROM {self.table_name}'
        self.cursor.execute(query)
        self.logger.info(f'"{self.table_name}" has been cleared')

    def insert(self, song_data: SongData):
        """Вставка значения из song_data в таблицу"""
        keys = f'{", ".join(f"{key}" for key in song_data.__dict__.keys())}'
        values = list(map(str, song_data.__dict__.values()))
        count_values = f'{", ".join("?" for _ in values)}'
        query = f'INSERT INTO {self.table_name} ({keys}) VALUES ({count_values})'
        self.cursor.execute(query, values)
        self.logger.debug(f'"{song_data.artist} - {song_data.title}" has been added to table "{self.table_name}"')

    def delete(self, song_id: int):
        """Удаление элемента по id"""
        query = f'DELETE FROM {self.table_name} WHERE song_id=?'
        self.logger.debug(f'Song with id={song_id} has been deleted from table "{self.table_name}"')
        self.cursor.execute(query, [song_id])

    def find(self, condition: str = None) -> list:
        """
            Нахождение элементов по condition (в формате 'song_id = 1'), либо вообще всей таблички, если condition=None
        """
        if condition:
            query = f'SELECT * FROM {self.table_name} WHERE {condition}'
        else:
            query = f'SELECT * FROM {self.table_name}'
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        self.logger.info(f'{len(results)} rows was found in table "{self.table_name}" for {condition=}')

        return results

    def update(self, condition: str, new: str):
        query = f'UPDATE {self.table_name} SET {new} WHERE {condition}'
        self.logger.debug(f'Update table "{self.table_name}" where {condition} with new parameters {new}')
        self.cursor.execute(query)

    def find_duplicates(self):
        query = f'''
            SELECT title, artist, COUNT(*)
            FROM {self.table_name}
            GROUP BY artist, title
            HAVING COUNT(*) > 1;
        '''
        self.cursor.execute(query)
        results = self.cursor.fetchall()
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
