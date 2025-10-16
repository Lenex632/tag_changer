import os

from pathlib import Path

import pytest

from model import SongData
from tag_changer import TagChanger
from logger import set_up_logger_config


set_up_logger_config()


# TODO:
# Попробовать сделать отдельный конфиг со всеми данными, а тут просто тесты
# Остались ещё функции: change_tags, start
# У get_image и delete_images надо бы ещё проверку через логи сделать
# Надо ещё смотреть как каждая функция при ошибках себя ведёт.
#   И вообще задуматься как должны они себя при ошибках вести.
#   Полюбому надо логировать + может данные для UI подготавливать.
#   А должны ли мы падать при этом? Останавливать скрипт? Или как-то продолжать работу?
class TestTagChanger:
    target_dir = Path('/mnt/c/code/tag_changer/test_target_dir/')
    artist_dirs = ['Легенды', 'Legend']

    datas_1 = [
        ('12. Artist - Title', 'Artist - Title'),
        ('12) Artist - Title', 'Artist - Title'),
        ('12)Artist - Title', 'Artist - Title'),
        ('12 - Artist - Title', 'Artist - Title'),
        ('12- Artist - Title', 'Artist - Title'),
        ('12 -Artist - Title', '-Artist - Title'),
        ('12Artist - Title', '12Artist - Title'),
        ('Sum41 - Title', 'Sum41 - Title'),
        ('Sum 41 - Title', 'Sum 41 - Title'),
        ('41 Sum 41 - 41', 'Sum 41 - 41'),
        ('41 - Sum 41 - 41', 'Sum 41 - 41'),
        ('41) Sum 41 - 41', 'Sum 41 - 41')
    ]
    datas_2 = [
        ('1. Title', 'Title'),
        ('1)Title', 'Title'),
        ('1) Title', 'Title'),
        ('1 - Title', 'Title'),
        ('1- Title', 'Title'),
        ('1 -Title', '-Title'),
        ('1) +-', '+-'),
        ('1. +-', '+-'),
        ('1 - +-', '+-'),
        ('1- +-', '+-'),
        ('1)+-', '+-'),
        ('Sum 41', 'Sum 41'),
        ('Sum41', 'Sum41'),
        ('41Sum', '41Sum'),
        ('41) 41', '41'),
        ('41. 41', '41'),
        ('41 - 41', '41'),
        ('41- 41', '41'),
        ('name w-o number', 'name w-o number'),
        ('name w - o number', 'name w - o number'),
    ]
    datas_3 = [
        ('41 Sum', 'Sum'),
        ('12.Artist - Title', '12.Artist - Title'),
        ('12 Artist - Title', 'Artist - Title'),
    ]
    datas_4 = [
        ('Artist - Title', ('Artist', 'Title')),
        ('Artist - Titleft (feat. Man)', ('Artist', 'Titleft (feat. Man)')),
        ('Artist - Title (OP One Piece)', ('Artist', 'Title (OP One Piece)')),
        ('Title', ('', 'Title')),
        ('name w - o number', ('name w', 'o number')),
    ]
    datas_5 = [
        # раздельно
        ('Artistfeat featOther', ('Artistfeat featOther', [])),
        ('Artist feat Other', ('Artist', ['Other'])),
        ('Artist feat. Other', ('Artist', ['Other'])),
        ('Artist feat.Other', ('Artist', ['Other'])),
        ('Artist ftOther', ('Artist ftOther', [])),
        ('Artistfeat ft Other', ('Artistfeat', ['Other'])),
        ('Artist ft. Other', ('Artist', ['Other'])),
        ('Artist ft.Other', ('Artist', ['Other'])),
        # в скобках
        ('Artistft (featOther)', ('Artistft (featOther)', [])),
        ('Artist (feat Other)', ('Artist', ['Other'])),
        ('Artist (feat. Other)', ('Artist', ['Other'])),
        ('Artist (feat.Other)', ('Artist', ['Other'])),
        ('Artist (ftOther)', ('Artist (ftOther)', [])),
        ('Artist (ft Other)', ('Artist', ['Other'])),
        ('Artistft (ft. Other)', ('Artistft', ['Other'])),
        ('Artist (ft.Other)', ('Artist', ['Other'])),
        # в скобках слитно
        ('Artist(featOther)', ('Artist(featOther)', [])),
        ('Artistft(feat Other)', ('Artistft', ['Other'])),
        ('Artist(feat. Other)', ('Artist', ['Other'])),
        ('Artist(feat.Other)', ('Artist', ['Other'])),
        ('Artistfeat(ftOther)', ('Artistfeat(ftOther)', [])),
        ('Artist(ft Other)', ('Artist', ['Other'])),
        ('Artist(ft. Other)', ('Artist', ['Other'])),
        ('Artist(ft.Other)', ('Artist', ['Other'])),
        # несколько исполнителей в feat
        ('Artist (feat. Other1, Other2)', ('Artist', ['Other1', 'Other2'])),
        ('Artistft ftOther (feat. Man)', ('Artistft ftOther', ['Man'])),
        ('Artistft (ftOther) (feat. Dave)', ('Artistft (ftOther)', ['Dave'])),
        # обработка Title
        ('Titleft (feat. Other1, Other2)', ('Titleft', ['Other1', 'Other2'])),
    ]
    datas_6 = [
        ('Title (EN One Piece)', ('Title', '(EN One Piece)')),
        ('Title (OP One Piece)', ('Title', '(OP One Piece)')),
        ('Title (OPOne Piece)', ('Title (OPOne Piece)', '')),
        ('Title (OP 1)', ('Title', '(OP 1)')),
        ('Title (EN 1)', ('Title', '(EN 1)')),
        ('Title (OP1)', ('Title', '(OP1)')),
        ('Title (EN1)', ('Title', '(EN1)')),
    ]
    datas_7 = [
        ('Artist - Title', 'Artist - Title'),
        ('Artist - Title(Garbage)', 'Artist - Title'),
        ('Artist - Title[Garbage]', 'Artist - Title'),
        ('Artist - Title (Garbage)', 'Artist - Title'),
        ('Artist - Title [Garbage]', 'Artist - Title'),
        ('Title(Garbage)', 'Title'),
        ('(NotGarbage)Title', '(NotGarbage)Title'),
        ('[NotGarbage]Title', '[NotGarbage]Title'),
        ('Title[Garbage]', 'Title'),
        ('Title (Garbage)', 'Title'),
        ('Title [Garbage]', 'Title'),
        ('Tit (NotGarbage) le', 'Tit (NotGarbage) le'),
        ('Tit [NotGarbage] le', 'Tit [NotGarbage] le'),
        ('Artist - The (S)hift', 'Artist - The (S)hift'),
        ('Artist - The [S]hift', 'Artist - The [S]hift'),
        ('Artist - The Sh(i)ft', 'Artist - The Sh(i)ft'),
        ('Artist - The Sh[i]ft', 'Artist - The Sh[i]ft'),
    ]
    datas_8 = [
        ('Artist - Title[Garbage)', 'Artist - Title[Garbage)'),
        ('Artist - Title(Garbage]', 'Artist - Title(Garbage]'),
        ('(Garbage) Title', 'Title'),
        ('[Garbage] Title', 'Title'),
    ]
    datas_9 = [
        ('Artist, Other2, Other3', ('Artist', ['Other2', 'Other3'])),
        ('Artist,Other2,Other3', ('Artist', ['Other2', 'Other3'])),
    ]
    datas_10 = [
        (('Title', 'Other2, Other3', '(EN One Piece)'), 'Title (feat. Other2, Other3) (EN One Piece)'),
        (('Title', '', ''), 'Title'),
        (('Title', 'Other2', ''), 'Title (feat. Other2)'),
        (('Title', '', '(EN One Piece)'), 'Title (EN One Piece)'),
    ]
    datas_11 = [
        ((Path(f'{target_dir}/The Best'), 'The Best'), Path(f'{target_dir}/The Best/The Best.jpg')),
        ((Path(f'{target_dir}/The Best/album'), 'album'), None),
        ((Path(f'{target_dir}/Legend/artist/album 1'), 'album 1'), Path(f'{target_dir}/Legend/artist/album 1/album 1.jpg')),
        ((Path(f'{target_dir}/Legend/artist/album_2'), 'album_2'), Path(f'{target_dir}/Legend/artist/album_2/album_2.jpg')),
        ((Path(f'{target_dir}/Legend/Saint Asonia'), 'Saint Asonia'), Path(f'{target_dir}/Legend/Saint Asonia/Saint Asonia.jpg')),
    ]
    datas_12 = [
        (
            Path(f'{target_dir}/Legend/Saint Asonia/Saint Asonia,Sharon den Adel - Sirens.mp3'),
            SongData(
                file_path=Path('Legend/Saint Asonia/Saint Asonia/Saint Asonia,Sharon den Adel - Sirens.mp3'),
                title='Sirens',
                artist='Saint Asonia',
                album='Saint Asonia',
                feat='Sharon den Adel',
                special='',
                image=Path(f'{target_dir}/Legend/Saint Asonia/Saint Asonia/Saint Asonia.jpg')
            )
        ),
        (
            Path(f'{target_dir}/Legend/artist/album 1/1. title 1.mp3'),
            SongData(
                file_path=Path('Legend/artist/album 1/1. title 1.mp3'),
                title='title 1',
                artist='artist',
                album='album 1',
                feat='',
                special='',
                image=Path(f'{target_dir}/Legend/artist/album 1/album 1.jpg')
            ),
        ),
        (
            Path(f'{target_dir}/Legend/artist/album_2/2 - title2 (feat. artist).mp3'),
            SongData(
                file_path=Path('Legend/artist/album_2/2 - title2 (feat. artist).mp3'),
                title='title2',
                artist='artist',
                album='album_2',
                feat='artist',
                special='',
                image=Path(f'{target_dir}/Legend/artist/album_2/album_2.jpg')
            ),
        ),
        (
            Path(f'{target_dir}/Legend/artist/album 1/3 title3 (Japan Version).mp3'),
            SongData(
                file_path=Path('Legend/artist/album 1/3 title3 (Japan Version).mp3'),
                title='title3',
                artist='artist',
                album='album 1',
                feat='',
                special='',
                image=Path(f'{target_dir}/Legend/artist/album 1/album 1.jpg')
            ),
        ),
        (
            Path(f'{target_dir}/OSU/Blech/EMPiRE - RiGHT NOW (EN9).mp3'),
            SongData(
                file_path=Path('OSU/Blech/EMPiRE - RiGHT NOW (EN9).mp3'),
                title='RiGHT NOW',
                artist='EMPiRE',
                album='Blech',
                feat='',
                special='(EN9)',
                image=None
            ),
        ),
        (
            Path(f'{target_dir}/Legend/artist/album_2/6 - +-0.mp3'),
            SongData(
                file_path=Path('Legend/artist/album_2/6 - +-0.mp3'),
                title='+-0',
                artist='artist',
                album='album_2',
                feat='',
                special='',
                image=Path(f'{target_dir}/Legend/artist/album_2/album_2.jpg')
            ),
        ),
        (
            Path(f'{target_dir}/Legend/artist/album_2/45.mp3'),
            SongData(
                file_path=Path('Legend/artist/album_2/45.mp3'),
                title='45',
                artist='artist',
                album='album_2',
                feat='',
                special='',
                image=Path(f'{target_dir}/Legend/artist/album_2/album_2.jpg')
            ),
        ),
        (
            Path(f'{target_dir}/Legend/artist/album_2/name w-o number.mp3'),
            SongData(
                file_path=Path('Legend/artist/album_2/name w-o number.mp3'),
                title='name w-o number',
                artist='artist',
                album='album_2',
                feat='',
                special='',
                image=Path(f'{target_dir}/Legend/artist/album_2/album_2.jpg')
            ),
        ),
        (
            Path(f'{target_dir}/The Best/The Score, Awolnation - Carry On (feat. SomeOne, Awolnation).mp3'),
            SongData(
                file_path=Path('The Best/The Score, Awolnation - Carry On (feat. SomeOne, Awolnation).mp3'),
                title='Carry On',
                artist='The Score',
                album='The Best',
                feat='Awolnation, SomeOne, Awolnation',  # WARN: а вот такого вообще быть не должно...
                special='',
                image=Path(f'{target_dir}/The Best/The Best.jpg')
            ),
        ),
        (
            Path(f'{target_dir}/The Best/album/1. artist - title (garbge).mp3'),
            SongData(
                file_path=Path('The Best/album/1. artist - title (garbge).mp3'),
                title='title',
                artist='artist',
                album='album',
                feat='',
                special='',
                image=None
            )
        ),
    ]

    @pytest.fixture(scope='class')
    def tag_changer(self) -> TagChanger:
        tc = TagChanger()
        tc.target_dir = self.target_dir
        tc.artist_dirs = self.artist_dirs
        return tc

    @pytest.fixture(scope='class', autouse=True)
    def teardown(self, tag_changer):
        yield
        cmd = "rm -rf test_from_dir/ test_to_dir/ test_sync_dir_1/ test_sync_dir_2/ test_target_dir/ && \
            git restore test_from_dir/ test_to_dir/ test_sync_dir_1/ test_sync_dir_2/ test_target_dir/ \
            db/test.db db/music.db"
        os.system(cmd)

    @pytest.mark.parametrize('input, output', datas_1)
    def test_delete_numbers_with_artist(self, tag_changer, input, output):
        assert tag_changer.delete_numbers(input) == output

    @pytest.mark.parametrize('input, output', datas_2)
    def test_delete_numbers_without_artist(self, tag_changer, input, output):
        assert tag_changer.delete_numbers(input) == output

    @pytest.mark.parametrize('input, output', datas_3)
    def test_delete_numbers_special(self, tag_changer, input, output):
        # PERF: не уверен правильно ли это
        assert tag_changer.delete_numbers(input) == output

    @pytest.mark.parametrize('input, output', datas_4)
    def test_split_fullname(self, tag_changer, input, output):
        assert tag_changer.split_fullname(input) == output

    @pytest.mark.parametrize('input, output', datas_5)
    def test_find_feats(self, tag_changer, input, output):
        assert tag_changer.find_feats(input) == output

    @pytest.mark.parametrize('input, output', datas_6)
    def test_find_anime(self, tag_changer, input, output):
        assert tag_changer.find_special(input) == output

    @pytest.mark.parametrize('input, output', datas_7)
    def test_delete_brackets(self, tag_changer, input, output):
        assert tag_changer.delete_brackets(input) == output

    @pytest.mark.skip(reason='Не знаю правильно ли это')
    @pytest.mark.parametrize('input, output', datas_8)
    def test_delete_brackets_special(self, tag_changer, input, output):
        assert tag_changer.delete_brackets(input) == output

    @pytest.mark.parametrize('input, output', datas_9)
    def test_split_artist(self, tag_changer, input, output):
        assert tag_changer.split_artist(input) == output

    @pytest.mark.parametrize('input, output', datas_10)
    def test_merge(self, tag_changer, input, output):
        assert tag_changer.merge(*input) == output

    @pytest.mark.parametrize('input, output', datas_11)
    def test_get_image(self, tag_changer, input, output):
        # TODO: дописать тесты через вывод логов
        assert tag_changer.get_image(*input) == output

    @pytest.mark.parametrize('input, output', datas_12)
    def test_get_file_info(self, tag_changer, input, output):
        assert tag_changer.get_info_from_file(input) == output

    def test_delete_images(self, tag_changer):
        # TODO: дописать тесты через вывод логов
        tag_changer.delete_images(self.target_dir)

    # @pytest.mark.parametrize('input, output', datas_12)
    # def test_change_tags(self, tag_changer, input, output):
    #     assert tag_changer.change_tags(input) == output

