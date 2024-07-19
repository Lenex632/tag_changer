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
            print(self.connection)
            try:
                self.connection.commit()
            except Exception as e:
                self.logger.error(f'Cant commit changes to db "{self.db_name}". Error: {e}')
            finally:
                self.connection.close()

    def create_table_if_not_exists(self) -> None:
        table_columns = f'{", ".join(f"{key} {value}" for key, value in TableModel().__dict__.items())}'
        query = f'CREATE TABLE IF NOT EXISTS {self.table_name} ({table_columns})'
        self.cursor.execute(query)
        self.connection.commit()

    def clear_table(self):
        query = f'DELETE FROM {self.table_name}'
        self.cursor.execute(query)
        self.logger.info(f'"{self.table_name}" has been cleared')

    def insert(self, song_data: SongData):
        keys = f'{", ".join(f"{key}" for key in song_data.__dict__.keys())}'
        values = list(map(str, song_data.__dict__.values()))
        count_values = f'{", ".join("?" for _ in values)}'
        query = f'INSERT INTO {self.table_name} ({keys}) VALUES ({count_values})'
        self.cursor.execute(query, values)
        self.logger.debug(f'"{song_data.artist} - {song_data.title}" has been added to table "{self.table_name}"')

    def delete(self, song_id: int):
        query = f'DELETE FROM {self.table_name} WHERE song_id=?'
        self.logger.debug(f'Song with id={song_id} has been deleted from table "{self.table_name}"')
        self.cursor.execute(query, [song_id])


def delete_test():
    db = DBController()
    db.delete(4)


if __name__ == '__main__':
    from logger import set_up_logger_config
    set_up_logger_config()

    delete_test()
    # db.clear_table()