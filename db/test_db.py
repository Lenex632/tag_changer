from pathlib import Path
import pytest

from db_controller import DBController
from model import SongData


class TestDB:
    @pytest.fixture
    def db_name(self):
        return 'test.db'

    @pytest.fixture
    def normal_connection_to_db(self, db_name):
        return DBController(db_name=db_name)

    @pytest.fixture()
    def delete_test_db(self, db_name, normal_connection_to_db):
        yield True
        normal_connection_to_db.__del__()
        Path.unlink(Path(db_name))

    def test_insert(self, normal_connection_to_db):
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

    def test_delete(self, normal_connection_to_db, delete_test_db):
        db = normal_connection_to_db
        db.delete(1)
