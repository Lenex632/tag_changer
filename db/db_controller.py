import logging
import sqlite3

from dataclasses import asdict
from pathlib import Path

from model import SongData, TableModel


class DBController:
    def __init__(self, db_name: str = 'music') -> None:
        """
        Класс управления базой данных.
        Операции будут проводиться с помощью контекстного менеджера.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_name = db_name + '.db'
        self.db_path = Path(Path(__file__).parent, self.db_name)
        self.table_model = TableModel()

    def __enter__(self) -> "DBController":
        self.connection = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.logger.error(f'Не удалось зафиксировать изменения в базе данных: "{self.db_name}"')
                self.logger.critical(exc_type, exc_info=True)
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

    def create_table_if_not_exist(self, table: str) -> None:
        """Создаёт базу данных и таблицу table, если такие не существуют"""
        table_columns = f'{", ".join(f"{key} {value}" for key, value in asdict(self.table_model).items())}'
        # TODO: мб подправить хардкод с file_path
        query = (f'CREATE TABLE IF NOT EXISTS {table} ({table_columns}, '
                 f'CONSTRAINT unique_file_path UNIQUE (file_path))')
        self.logger.debug(f'Была созданна таблица: {table}')
        self.execute(query)

    def get_tables_list(self) -> list | tuple:
        """Возвращает имена всех несистемных таблиц из базы данных"""
        query = 'SELECT name FROM sqlite_master WHERE type="table" AND name NOT LIKE "sqlite_%"'
        results = self.execute_and_fetch(query)
        results = [res[0] for res in results]
        self.logger.debug(f'Список таблиц в базе: {results}')
        return results

    def clear_table(self, table: str) -> None:
        """Очищение таблицы от всех данных"""
        query = f'DELETE FROM {table}'
        self.execute(query)
        self.logger.debug(f'Таблица была очищена: "{table}"')

    def drop_table(self, table: str) -> None:
        """Удаляет выбранную таблицу"""
        query = f'DROP TABLE IF EXISTS {table}'
        self.execute(query)
        self.logger.debug(f'Таблица была удалена: "{table}"')

    def insert(self, table: str, song_data: SongData) -> None:
        """Вставка значений song_data в таблицу"""
        # Подготовка значений, а то sqlite3 будет ругаться
        song_data.file_path = str(song_data.file_path)
        data_dict = asdict(song_data)
        # PERF: хардкод с image
        data_dict.pop('image')

        keys = ', '.join(data_dict.keys())
        values = tuple(data_dict.values())
        query = f'INSERT INTO {table} ({keys}) VALUES ({", ".join("?" for _ in values)})'
        self.execute(query, params=values)
        self.logger.debug(f'"{song_data.artist} - {song_data.title}" была добавлена в таблицу "{table}"')

    def delete(self, table: str, song_id: int) -> None:
        """Удаление элемента по id"""
        query = f'DELETE FROM {table} WHERE song_id={song_id}'
        self.execute(query)
        self.logger.debug(f'Данные были удалены {song_id=} из таблицы "{table}"')

    def find(self, table: str, condition: str = None) -> list:
        """
        Нахождение элементов по condition (в формате 'song_id = 1'),
        либо вообще всей таблички, если condition=None
        ВНИМАНИИЕ! строковые представления в condition
                   должны заключаться в одинарные кавычки
        """
        if condition:
            query = f'SELECT * FROM {table} WHERE {condition}'
        else:
            query = f'SELECT * FROM {table}'
        results = self.execute_and_fetch(query)
        self.logger.debug(f'Было найдено {len(results)} совпадений в "{table}" для условия {condition or "ALL"}')
        self.logger.debug(results)
        return results

    def update(self, table: str, condition: str, new: str) -> None:
        """
        Нахождение элемента с condition (в формате 'song_id = 1') и обновление его
        параметров new (в формате 'title = "New Title"')
        ВНИМАНИИЕ! строковые представления в condition
                   должны заключаться в одинарные кавычки
        """
        query = f'UPDATE {table} SET {new} WHERE {condition}'
        self.logger.debug(f'В элементах с условием {condition} в таблице {table} были обновлены параметры: {new}')
        self.execute(query)

    def find_duplicates(self, table: str) -> list[tuple]:
        query = f'''
            SELECT title, artist, COUNT(*)
            FROM {table}
            GROUP BY artist, title
            HAVING COUNT(*) > 1;
        '''
        results = self.execute_and_fetch(query)
        self.logger.debug(f'{len(results)} групп дубликатов было найдено в таблице "{table}"')
        duplicates = []
        for res in results:
            title = res[0]
            artist = res[1]
            condition = f"title = '{title}' AND artist = '{artist}'"
            duplicate = self.find(table, condition)
            duplicates.append((title, artist, duplicate))
        self.logger.debug(f'Дубликаты:\n{duplicates}')
        return duplicates

    def find_differences(self, library1: str, library2: str) -> [list, list]:
        # TODO: всё ещё надо адаптировать
        query = f'''SELECT file_path from {library1};'''
        dif1 = self.execute_and_fetch(query)
        query = f'''SELECT file_path from {library2};'''
        dif2 = self.execute_and_fetch(query)

        print(len(dif1), '---------------------')
        for d in dif1:
            print(d)
        print(len(dif2), '---------------------')
        for d in dif2:
            print(d)

        query = f'''
            SELECT {library1}.file_path, {library2}.file_path
            FROM {library1} LEFT JOIN {library2}
            ON {library1}.file_path = {library2}.file_path
            UNION
            SELECT {library1}.file_path, {library2}.file_path
            FROM {library2} LEFT JOIN {library1}
            ON {library1}.file_path = {library2}.file_path;
        '''
        result = self.execute_and_fetch(query)
        print('------------------------------------')
        for res in result:
            print(res)

        dif1, dif2 = [], []
        for dir1, dir2 in result:
            if dir1 is None:
                dif1.append(dir2)
            if dir2 is None:
                dif2.append(dir1)
        print('------------------------------------')
        for d in dif1:
            print(d)
        print('------------------------------------')
        for d in dif2:
            print(d)

        return dif1, dif2


def test_create() -> None:
    with DBController(db_name='test') as db:
        db.create_table_if_not_exist('test')
        db.get_tables_list()
        db.drop_table('test')


def test_insert() -> None:
    song_data = SongData(
        file_path=Path('The Best\\test album\\EMPiRE - RiGHT NOW (EN9).mp3'),
        title='RiGHT NOW',
        artist='EMPiRE',
        album='test album',
        feat='',
        image=Path('The Best\\test album\\test album.jpg')
    )
    with DBController(db_name='test') as db:
        db.create_table_if_not_exist('main')
        db.insert('main', song_data)
        db.find('main', 'album = "test album"')
        db.update('main', "album = 'test album'", "album = 'test album 2'")
        db.find('main', "album = 'test album'")
        db.find('main', "album = 'test album 2'")
        db.delete('main', 1)
        db.find('main')
        db.drop_table('main')


def test_duplicates() -> None:
    with DBController(db_name='music') as db:
        db.find_duplicates('target_dir')


def test_some() -> None:
    with DBController(db_name='music') as db:
        db.find('target_dir', "artist = 'artist'")


if __name__ == '__main__':
    from logger import set_up_logger_config
    set_up_logger_config()

    # test_create()
    # test_insert()
    test_duplicates()
    # test_some()

