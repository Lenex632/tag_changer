import os

from pathlib import Path

import pytest

from db import DBController
from tag_changer import TagChanger
from model import SongData
from logger import set_up_logger_config


set_up_logger_config()


# TODO: в них теперь чёрт ногу сломает, но я хз как сделать лучше =_=
# create_table_if_not_exist, get_tables_list, clear_table, drop_table,
# find_differences
class TestDB:
    target_datas = [
        (1, 'Legend/artist/album 1/1. title 1.mp3', 'title 1', 'artist', 'album 1', '', ''),
        (2, 'Legend/artist/album 1/15. title 15 (Just Another Name).mp3', 'title 15', 'artist', 'album 1', '', ''),
        (3, 'Legend/artist/album 1/2 - title2 (feat. artist).mp3', 'title2', 'artist', 'album 1', 'artist', ''),
        (4, 'Legend/artist/album 1/3 title3 (Japan Version).mp3', 'title3', 'artist', 'album 1', '', ''),
        (5, 'Legend/artist/album 1/4) title 4 (ft. some one).mp3', 'title 4', 'artist', 'album 1', 'some one', ''),
        (6, 'Legend/artist/album 1/5. title5 (Just Another Name).mp3', 'title5', 'artist', 'album 1', '', ''),
        (7, 'Legend/artist/album_2/1. title 1.mp3', 'title 1', 'artist', 'album_2', '', ''),
        (8, 'Legend/artist/album_2/2 - title2 (feat. artist).mp3', 'title2', 'artist', 'album_2', 'artist', ''),
        (9, 'Legend/artist/album_2/3 title3 (Japan Version).mp3', 'title3', 'artist', 'album_2', '', ''),
        (10, 'Legend/artist/album_2/4) title 4 (feat. some one).mp3', 'title 4', 'artist', 'album_2', 'some one', ''),
        (11, 'Legend/artist/album_2/45.mp3', '45', 'artist', 'album_2', '', ''),
        (12, 'Legend/artist/album_2/5. title5 (Just Another Name).mp3', 'title5', 'artist', 'album_2', '', ''),
        (13, 'Legend/artist/album_2/6 - +-0.mp3', '+-0', 'artist', 'album_2', '', ''),
        (14, 'Legend/artist/album_2/7 +-0.mp3', '+-0', 'artist', 'album_2', '', ''),
        (15, 'Legend/artist/album_2/name w-o number.mp3', 'name w-o number', 'artist', 'album_2', '', ''),
        (16, 'Legend/Saint Asonia/Saint Asonia/Saint Asonia - Waste My Time.mp3', 'Waste My Time', 'Saint Asonia', 'Saint Asonia', '', ''),
        (17, 'Legend/Saint Asonia/Flawed Design/Saint Asonia - Weak & Tired.mp3', 'Weak & Tired', 'Saint Asonia', 'Flawed Design', '', ''),
        (18, 'Legend/Saint Asonia/Saint Asonia/Saint Asonia,Sharon den Adel - Sirens.mp3', 'Sirens', 'Saint Asonia', 'Saint Asonia', 'Sharon den Adel', ''),
        (19, 'OSU/AK, Lynx, Veela - Virtual Paradise.mp3', 'Virtual Paradise', 'AK', 'OSU', 'Lynx, Veela', ''),
        (20, 'OSU/Blech/EMPiRE - RiGHT NOW (EN9).mp3', 'RiGHT NOW', 'EMPiRE', 'Blech', '', '(EN9)'),
        (21, 'OSU/Blech/Koda Kumi - Guess Who Is Back (OP4).mp3', 'Guess Who Is Back', 'Koda Kumi', 'Blech', '', '(OP4)'),
        (22, 'OSU/Blech/Snow Man - Grandeur (OP13).mp3', 'Grandeur', 'Snow Man', 'Blech', '', '(OP13)'),
        (23, 'OSU/Blech/TOMORROW X TOGETHER - Everlasting Shine (OP12).mp3', 'Everlasting Shine', 'TOMORROW X TOGETHER', 'Blech', '', '(OP12)'),
        (24, 'OSU/Blech/Vickeblanka - Black Catcher (OP10).mp3', 'Black Catcher', 'Vickeblanka', 'Blech', '', '(OP10)'),
        (25, 'OSU/Blech/Vickeblanka - Black Rover (OP3).mp3', 'Black Rover', 'Vickeblanka', 'Blech', '', '(OP3)'),
        (26, 'OSU/Eve - Fight Song.mp3', 'Fight Song', 'Eve', 'OSU', '', ''),
        (27, 'OSU/One Ok Rock - 20-20.mp3', '20-20', 'One Ok Rock', 'OSU', '', ''),
        (28, 'OSU/Porter Robinson - Shelter (ft. Madeon).mp3', 'Shelter', 'Porter Robinson', 'OSU', 'Madeon', ''),
        (29, 'The Best/album/1. artist - title (garbge).mp3', 'title', 'artist', 'album', '', ''),
        (30, 'The Best/album/2 artist - title.mp3', 'title', 'artist', 'album', '', ''),
        (31, 'The Best/album/3) artist - title.mp3', 'title', 'artist', 'album', '', ''),
        (32, 'The Best/Almos Awesome - Alive.mp3', 'Alive', 'Almos Awesome', 'The Best', '', ''),
        (33, 'The Best/GTA V/All Saints - Pure Shores.mp3', 'Pure Shores', 'All Saints', 'GTA V', '', ''),
        (34, 'The Best/GTA V/Battle Tapes - Feel the Same.mp3', 'Feel the Same', 'Battle Tapes', 'GTA V', '', ''),
        (35, 'The Best/Ren - Hi Ren.mp3', 'Hi Ren', 'Ren', 'The Best', '', ''),
        (36, "The Best/Surf Up/A - Something's Going On.mp3", "Something's Going On", 'A', 'Surf Up', '', ''),
        (37, "The Best/Surf Up/Plain White T's - Down the Road.mp3", 'Down the Road', "Plain White T's", 'Surf Up', '', ''),
        (38, 'The Best/The Score, Awolnation - Carry On (feat. SomeOne, Awolnation).mp3', 'Carry On', 'The Score', 'The Best', 'Awolnation, SomeOne, Awolnation', ''),
        (39, 'Легенды/Linkin Park/Meteora/1. Meteora.mp3', 'Meteora', 'Linkin Park', 'Meteora', '', ''),
        (40, 'Легенды/Linkin Park/Meteora/2 - Numb.mp3', 'Numb', 'Linkin Park', 'Meteora', '', ''),
        (41, "Легенды/Linkin Park/Meteora/3) What I've Done.mp3", "What I've Done", 'Linkin Park', 'Meteora', '', ''),
        (42, 'Легенды/Linkin Park/Hybrid Theory/4 Bleed It Out.mp3', 'Bleed It Out', 'Linkin Park', 'Hybrid Theory', '', ''),
        (43, 'Легенды/Linkin Park/Hybrid Theory/5. Breaking the Habit.mp3', 'Breaking the Habit', 'Linkin Park', 'Hybrid Theory', '', ''),
        (44, 'Легенды/Linkin Park/Hybrid Theory/6 Burn it Down.mp3', 'Burn it Down', 'Linkin Park', 'Hybrid Theory', '', '')
    ]
    next_idx = len(target_datas) + 1
    new_song_datas = [
        (
            SongData(
                file_path=Path('The Best/new_artist - new_title.mp3'),
                title='new_title',
                artist='new_artist',
                album='The Best',
                feat='',
                special='',
                image=Path('The Best/The Best.jpg')
            ),
            (next_idx, 'The Best/new_artist - new_title.mp3', 'new_title', 'new_artist', 'The Best', '', '')
        ),
        (
            SongData(
                file_path=Path('Legend/artist/album 1/1. title 1.mp3'),
                title='title 1',
                artist='artist',
                album='album 1',
                feat='',
                special='',
                image=Path('artist/album 1/album 1.jpg')
            ),
            (1, 'Legend/artist/album 1/1. title 1.mp3', 'title 1', 'artist', 'album 1', '', '')
        ),
        (
            SongData(
                file_path=Path('The Best/another_artist - another_title.mp3'),
                title='another_title',
                artist='another_artist',
                album='The Best',
                feat='',
                special='',
                image=Path('The Best/The Best.jpg')
            ),
            (target_datas[1][0], 'The Best/another_artist - another_title.mp3', 'another_title', 'another_artist', 'The Best', '', '')
        ),
        SongData(
            file_path=Path('Legend/artist/album_2/5. Name5 (Just Another Name).mp3'),
            title='Name5',
            artist='artist',
            album='album_2',
            feat='',
            special='',
            image=None
        ),
        SongData(
            file_path=Path('some/other/path/EMPiRE - RiGHT NOW (EN9).mp3'),
            title='RiGHT NOW',
            artist='EMPiRE',
            album='album',
            feat='',
            special='(EN9)',
            image=Path('some/other/path/album.jpg')
        ),
    ]

    datas_1 = [
        (None, target_datas),
        (f'song_id = {target_datas[0][0]}', target_datas[0]),
        (f'title = "{target_datas[14][2]}"', target_datas[14]),
        # TODO: тут тоже можно как-нить от хардкода уйти
        ('artist = "Linkin Park"', target_datas[38:44]),
    ]
    datas_2 = [
        (new_song_datas[0][0], new_song_datas[0][1]),
        # TODO: надо подумать как быть с повторюшками
        pytest.param(
            new_song_datas[1][0],
            new_song_datas[1][1],
            marks=pytest.mark.skip('надо подумать как быть с повторяющимися')
        ),
    ]
    datas_3 = [
        (target_datas[1], new_song_datas[2][1][1:], new_song_datas[2][1]),
    ]

    @pytest.fixture(scope='class')
    def db_name(self):
        return 'test'

    @pytest.fixture(scope='class')
    def target_lib(self):
        return 'target_lib'

    @pytest.fixture(scope='class')
    def target_dir(self):
        return Path('/mnt/c/code/tag_changer/test_target_dir/')

    @pytest.fixture(scope='class')
    def artist_dirs(self):
        return ['Легенды', 'Legend']

    @pytest.fixture(scope='class', autouse=True)
    def prepare_env(self, db_name, target_dir, target_lib, artist_dirs):
        tc = TagChanger()
        tc.target_dir = target_dir
        tc.artist_dirs = artist_dirs
        items = tc.start(target_dir)
        with DBController(db_name=db_name) as db:
            db.drop_table(db_name)
            db.create_table_if_not_exist(target_lib)
            for song_data in items:
                db.insert(target_lib, song_data)
        tc.delete_images(target_dir)
        yield

        cmd = "rm -rf test_from_dir/ test_to_dir/ test_sync_dir_1/ test_sync_dir_2/ test_target_dir/ && \
            git restore test_from_dir/ test_to_dir/ test_sync_dir_1/ test_sync_dir_2/ test_target_dir/ \
            db/test.db db/music.db"
        os.system(cmd)

    @pytest.fixture
    def db_connection(self, db_name):
        return DBController(db_name=db_name)

    @pytest.mark.parametrize('input, output', datas_1)
    def test_find(self, db_connection, target_lib, input, output):
        with db_connection as db:
            results = db.find(target_lib, input)
        assert results == output

    @pytest.mark.parametrize('input, output', datas_2)
    def test_insert(self, db_connection, target_lib, input, output):
        with db_connection as db:
            db.insert(target_lib, input)
            results = db.find(target_lib)
        assert len(results) == self.next_idx
        with db_connection as db:
            results = db.find(target_lib, f'song_id = {self.next_idx}')
        assert results == output

    @pytest.mark.parametrize('before, input, after', datas_3)
    def test_update(self, db_connection, target_lib, before, input, after):
        with db_connection as db:
            results = db.find(target_lib, f'song_id = {before[0]}')
        assert results == before
        with db_connection as db:
            path, title, artist, album, feat, special = input
            db.update(
                target_lib,
                f'song_id = {before[0]}',
                f'file_path = "{path}", title = "{title}", artist = "{artist}", \
                album = "{album}", feat = "{feat}", special = "{special}"'
            )
            results = db.find(target_lib, f'song_id = {before[0]}')
        assert results == after

    def test_delete(self, db_connection, target_lib):
        with db_connection as db:
            before = db.find(target_lib)
            db.delete(target_lib, self.next_idx - 1)
            after = db.find(target_lib)
        assert len(after) == len(before) - 1

    # TODO: ну тут уже нахардкодил
    def test_find_duplicates(self, db_connection, target_lib):
        with db_connection as db:
            results = db.find_duplicates(target_lib)
        assert len(results) == 7

    # def test_find_differences(self, db_connection, target_lib):
    #     with db_connection as db:
    #         results = db.find_differences(target_lib)
    #     assert len(results) == 7

    def test_clear_table(self, db_connection, target_lib):
        with db_connection as db:
            before = db.find(target_lib)
        assert len(before) != 0
        with db_connection as db:
            db.clear_table(target_lib)
            after = db.find(target_lib)
        assert len(after) == 0

