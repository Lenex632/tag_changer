from pathlib import Path
import pytest

from db_controller import DBController
from model import SongData
from logger import set_up_logger_config


class TestDB:
    @pytest.fixture
    def db_name(self):
        set_up_logger_config()
        return 'test.db'

    @pytest.fixture
    def normal_connection_to_db(self, db_name):
        return DBController(db_name=db_name)

    @pytest.fixture()
    def delete_test_db(self, db_name, normal_connection_to_db):
        yield True
        normal_connection_to_db.__del__()
        Path.unlink(Path(db_name))

    def test_insert_and_find(self, normal_connection_to_db):
        db = normal_connection_to_db
        db.insert(SongData(
            file_path=Path('The Best\\test album\\EMPiRE - RiGHT NOW (EN9).mp3'),
            title='RiGHT NOW',
            artist='EMPiRE',
            album='test album',
            feat=[],
            special='(EN9)',
            image=Path('target_dir\\The Best\\test album\\test album.jpg')
        ))
        db.insert(SongData(
            file_path=Path('Legend\\Saint Asonia\\Flawed Design\\Saint Asonia,Sharon den Adel - Sirens.mp3'),
            title='Sirens',
            artist='Saint Asonia',
            album='Flawed Design',
            feat=['Sharon den Adel'],
            special='',
            image=Path('target_dir\\The Best\\test album\\test album.jpg')
        ))
        db.insert(SongData(
            file_path=Path('Legend\\test artist\\test_album_2\\5. Name5 (Just Another Name).mp3'),
            title='Name5',
            artist='test artist',
            album='test_album_2',
            feat=[],
            special='',
            image=Path(f'target_dir\\Legend\\test artist\\test_album_2\\test_album_2.jpg')
        ))

        results = db.find()
        assert len(results) == 3

        results = db.find('song_id = 1')
        assert results == [(
            1,
            'The Best\\test album\\EMPiRE - RiGHT NOW (EN9).mp3',
            'RiGHT NOW',
            'EMPiRE',
            'test album',
            '[]',
            '(EN9)',
            'target_dir\\The Best\\test album\\test album.jpg'
        )]

    def test_update(self, normal_connection_to_db):
        db = normal_connection_to_db

        results = db.find('song_id = 1')
        assert results[0][2] == 'RiGHT NOW'

        db.update('song_id = 1', 'title = "new_title"')
        results = db.find('song_id = 1')
        assert results[0][2] == 'new_title'

    def test_find_duplicates(self, normal_connection_to_db):
        db = normal_connection_to_db

        results = db.find_duplicates()
        assert len(results) == 0

        db.insert(SongData(
            file_path=Path('some\\other\\path\\EMPiRE - RiGHT NOW (EN9).mp3'),
            title='RiGHT NOW',
            artist='EMPiRE',
            album='test album',
            feat=[],
            special='(EN9)',
            image=Path('some\\other\\path\\test album.jpg')
        ))
        results = db.find_duplicates()
        assert len(results) == 1

    def test_delete(self, normal_connection_to_db):
        db = normal_connection_to_db

        results = db.find()
        assert len(results) == 3

        db.delete(1)
        results = db.find()
        assert len(results) == 2

    def test_clear_table(self, normal_connection_to_db, delete_test_db):
        db = normal_connection_to_db

        results = db.find()
        assert len(results) == 2

        db.clear_table()
        results = db.find()
        assert len(results) == 0
