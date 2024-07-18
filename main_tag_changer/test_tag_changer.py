from pathlib import Path

import pytest
from model import SongData
from tag_changer import TagChanger
from logger import set_up_logger_config


@pytest.fixture(scope="class")
def tag_changer():
    set_up_logger_config()
    return TagChanger('C:\\code\\tag_changer\\test_tag_change', ['Legend'])


class TestClass:
    def test_delete_numbers_with_artist(self, tag_changer):
        assert tag_changer.delete_numbers('12. Artist - Title') == 'Artist - Title'
        assert tag_changer.delete_numbers('12) Artist - Title') == 'Artist - Title'
        assert tag_changer.delete_numbers('12)Artist - Title') == 'Artist - Title'
        assert tag_changer.delete_numbers('12 - Artist - Title') == 'Artist - Title'
        assert tag_changer.delete_numbers('12- Artist - Title') == 'Artist - Title'
        assert tag_changer.delete_numbers('12 -Artist - Title') == '-Artist - Title'
        assert tag_changer.delete_numbers('12Artist - Title') == '12Artist - Title'
        assert tag_changer.delete_numbers('Sum41 - Title') == 'Sum41 - Title'
        assert tag_changer.delete_numbers('Sum 41 - Title') == 'Sum 41 - Title'
        assert tag_changer.delete_numbers('41 Sum 41 - 41') == 'Sum 41 - 41'
        assert tag_changer.delete_numbers('41) Sum 41 - 41') == 'Sum 41 - 41'
        assert tag_changer.delete_numbers('41 - Sum 41 - 41') == 'Sum 41 - 41'

    def test_delete_numbers_without_artist(self, tag_changer):
        assert tag_changer.delete_numbers('1. Title') == 'Title'
        assert tag_changer.delete_numbers('1)Title') == 'Title'
        assert tag_changer.delete_numbers('1) Title') == 'Title'
        assert tag_changer.delete_numbers('1 - Title') == 'Title'
        assert tag_changer.delete_numbers('1- Title') == 'Title'
        assert tag_changer.delete_numbers('1 -Title') == '-Title'
        assert tag_changer.delete_numbers('1) +-') == '+-'
        assert tag_changer.delete_numbers('1. +-') == '+-'
        assert tag_changer.delete_numbers('1 - +-') == '+-'
        assert tag_changer.delete_numbers('1- +-') == '+-'
        assert tag_changer.delete_numbers('1)+-') == '+-'
        assert tag_changer.delete_numbers('Sum 41') == 'Sum 41'
        assert tag_changer.delete_numbers('Sum41') == 'Sum41'
        assert tag_changer.delete_numbers('41Sum') == '41Sum'
        assert tag_changer.delete_numbers('41) 41') == '41'
        assert tag_changer.delete_numbers('41. 41') == '41'
        assert tag_changer.delete_numbers('41 - 41') == '41'
        assert tag_changer.delete_numbers('41- 41') == '41'
        assert tag_changer.delete_numbers('name w-o number') == 'name w-o number'
        assert tag_changer.delete_numbers('name w - o number') == 'name w - o number'

    def test_delete_numbers_special(self, tag_changer):
        # TODO не уверен правильно ли это
        assert tag_changer.delete_numbers('41 Sum') == 'Sum'
        assert tag_changer.delete_numbers('12.Artist - Title') == '12.Artist - Title'
        assert tag_changer.delete_numbers('12 Artist - Title') == 'Artist - Title'

    def test_split_fullname(self, tag_changer):
        assert tag_changer.split_fullname('Artist - Title') == ('Artist', 'Title')
        assert tag_changer.split_fullname('Artist - Titleft (feat. Man)') == ('Artist', 'Titleft (feat. Man)')
        assert tag_changer.split_fullname('Artist - Title (OP One Piece)') == ('Artist', 'Title (OP One Piece)')
        assert tag_changer.split_fullname('Title') == ('', 'Title')
        assert tag_changer.split_fullname('name w - o number') == ('name w', 'o number')

    def test_find_feats(self, tag_changer):
        # раздельно
        assert tag_changer.find_feats('Artistfeat featOther') == ('Artistfeat featOther', [])
        assert tag_changer.find_feats('Artist feat Other') == ('Artist', ['Other'])
        assert tag_changer.find_feats('Artist feat. Other') == ('Artist', ['Other'])
        assert tag_changer.find_feats('Artist feat.Other') == ('Artist', ['Other'])
        assert tag_changer.find_feats('Artist ftOther') == ('Artist ftOther', [])
        assert tag_changer.find_feats('Artistfeat ft Other') == ('Artistfeat', ['Other'])
        assert tag_changer.find_feats('Artist ft. Other') == ('Artist', ['Other'])
        assert tag_changer.find_feats('Artist ft.Other') == ('Artist', ['Other'])
        # в скобках
        assert tag_changer.find_feats('Artistft (featOther)') == ('Artistft (featOther)', [])
        assert tag_changer.find_feats('Artist (feat Other)') == ('Artist', ['Other'])
        assert tag_changer.find_feats('Artist (feat. Other)') == ('Artist', ['Other'])
        assert tag_changer.find_feats('Artist (feat.Other)') == ('Artist', ['Other'])
        assert tag_changer.find_feats('Artist (ftOther)') == ('Artist (ftOther)', [])
        assert tag_changer.find_feats('Artist (ft Other)') == ('Artist', ['Other'])
        assert tag_changer.find_feats('Artistft (ft. Other)') == ('Artistft', ['Other'])
        assert tag_changer.find_feats('Artist (ft.Other)') == ('Artist', ['Other'])
        # в скобках слитно
        assert tag_changer.find_feats('Artist(featOther)') == ('Artist(featOther)', [])
        assert tag_changer.find_feats('Artistft(feat Other)') == ('Artistft', ['Other'])
        assert tag_changer.find_feats('Artist(feat. Other)') == ('Artist', ['Other'])
        assert tag_changer.find_feats('Artist(feat.Other)') == ('Artist', ['Other'])
        assert tag_changer.find_feats('Artistfeat(ftOther)') == ('Artistfeat(ftOther)', [])
        assert tag_changer.find_feats('Artist(ft Other)') == ('Artist', ['Other'])
        assert tag_changer.find_feats('Artist(ft. Other)') == ('Artist', ['Other'])
        assert tag_changer.find_feats('Artist(ft.Other)') == ('Artist', ['Other'])
        # несколько исполнителей в feat
        assert (tag_changer.find_feats('Artist (feat. Other1, Other2)') == ('Artist', ['Other1', 'Other2']))
        assert tag_changer.find_feats('Artistft ftOther (feat. Man)') == ('Artistft ftOther', ['Man'])
        assert tag_changer.find_feats('Artistft (ftOther) (feat. Dave)') == ('Artistft (ftOther)', ['Dave'])
        # обработка Title
        assert tag_changer.find_feats('Titleft (feat. Other1, Other2)') == ('Titleft', ['Other1', 'Other2'])

    def test_find_anime(self, tag_changer):
        assert tag_changer.find_special('Title (EN One Piece)') == ('Title', '(EN One Piece)')
        assert tag_changer.find_special('Title (OP One Piece)') == ('Title', '(OP One Piece)')
        assert tag_changer.find_special('Title (OPOne Piece)') == ('Title (OPOne Piece)', '')
        assert tag_changer.find_special('Title (OP 1)') == ('Title', '(OP 1)')
        assert tag_changer.find_special('Title (EN 1)') == ('Title', '(EN 1)')
        assert tag_changer.find_special('Title (OP1)') == ('Title', '(OP1)')
        assert tag_changer.find_special('Title (EN1)') == ('Title', '(EN1)')

    def test_delete_brackets(self, tag_changer):
        assert tag_changer.delete_brackets('Artist - Title') == 'Artist - Title'
        assert tag_changer.delete_brackets('Artist - Title(Garbage)') == 'Artist - Title'
        assert tag_changer.delete_brackets('Artist - Title[Garbage]') == 'Artist - Title'
        assert tag_changer.delete_brackets('Artist - Title (Garbage)') == 'Artist - Title'
        assert tag_changer.delete_brackets('Artist - Title [Garbage]') == 'Artist - Title'
        assert tag_changer.delete_brackets('Title(Garbage)') == 'Title'
        assert tag_changer.delete_brackets('(NotGarbage)Title') == '(NotGarbage)Title'
        assert tag_changer.delete_brackets('[NotGarbage]Title') == '[NotGarbage]Title'
        assert tag_changer.delete_brackets('Title[Garbage]') == 'Title'
        assert tag_changer.delete_brackets('Title (Garbage)') == 'Title'
        assert tag_changer.delete_brackets('Title [Garbage]') == 'Title'
        assert tag_changer.delete_brackets('Tit (NotGarbage) le') == 'Tit (NotGarbage) le'
        assert tag_changer.delete_brackets('Tit [NotGarbage] le') == 'Tit [NotGarbage] le'
        assert tag_changer.delete_brackets('Artist - The (S)hift') == 'Artist - The (S)hift'
        assert tag_changer.delete_brackets('Artist - The [S]hift') == 'Artist - The [S]hift'
        assert tag_changer.delete_brackets('Artist - The Sh(i)ft') == 'Artist - The Sh(i)ft'
        assert tag_changer.delete_brackets('Artist - The Sh[i]ft') == 'Artist - The Sh[i]ft'

    @pytest.mark.skip(reason='не знаю правильно ли это')
    def test_delete_brackets_special(self, tag_changer):
        assert tag_changer.delete_brackets('Artist - Title[Garbage)') == 'Artist - Title[Garbage)'
        assert tag_changer.delete_brackets('Artist - Title(Garbage]') == 'Artist - Title(Garbage]'
        assert tag_changer.delete_brackets('(Garbage) Title') == 'Title'
        assert tag_changer.delete_brackets('[Garbage] Title') == 'Title'

    def test_split_artist(self, tag_changer):
        assert tag_changer.split_artist('Artist, Other2, Other3') == ('Artist', ['Other2', 'Other3'])
        assert tag_changer.split_artist('Artist,Other2,Other3') == ('Artist', ['Other2', 'Other3'])

    def test_merge(self, tag_changer):
        assert (tag_changer.merge('Title', ['Other2', 'Other3'], '(EN One Piece)')
                == 'Title (feat. Other2, Other3) (EN One Piece)')
        assert tag_changer.merge('Title', [], '') == 'Title'
        assert tag_changer.merge('Title', ['Other2'], '') == 'Title (feat. Other2)'
        assert tag_changer.merge('Title', [], '(EN One Piece)') == 'Title (EN One Piece)'

    def test_get_file_info(self, tag_changer):
        input_data = [
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\Saint Asonia\\Saint Asonia,Sharon den Adel - Sirens.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_2\\1. Name1.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_2\\2 - Name2 (feat. artist).mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_2\\3 Name3 (Japan Version).mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_2\\4 Name4 (OP1).mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_2\\'
            '5. Name5 (Just Another Name).mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_2\\6 - +-0.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_2\\7 +-0.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_2\\45.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_2\\name w-o number.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_2\\6 - +-0.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\The Best\\'
            'Taio Cruz, Some Artis, Some1 - Dynamite (feat. Some2).mp3',
            'C:\\code\\tag_changer\\test_tag_change\\The Best\\test album\\EMPiRE - RiGHT NOW (EN9).mp3'
        ]
        output_results = [
            SongData(
                file_path=Path('Legend\\Saint Asonia\\Saint Asonia,Sharon den Adel - Sirens.mp3'),
                title='Sirens',
                artist='Saint Asonia',
                album='Flawed Design',
                feat=['Sharon den Adel'],
                special='',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\'
                           'Legend\\Saint Asonia\\Flawed Design\\Flawed Design.jpg')
            ),
            SongData(
                file_path=Path('Legend\\test artist\\test_album_2\\1. Name1.mp3'),
                title='Name1',
                artist='test artist',
                album='test_album_2',
                feat=[],
                special='',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\'
                           'Legend\\test artist\\test_album_2\\test_album_2.jpg')
            ),
            SongData(
                file_path=Path('Legend\\test artist\\test_album_2\\2 - Name2 (feat. artist).mp3'),
                title='Name2',
                artist='test artist',
                album='test_album_2',
                feat=['artist'],
                special='',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\'
                           'Legend\\test artist\\test_album_2\\test_album_2.jpg')
            ),
            SongData(
                file_path=Path('Legend\\test artist\\test_album_2\\3 Name3 (Japan Version).mp3'),
                title='Name3',
                artist='test artist',
                album='test_album_2',
                feat=[],
                special='',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\'
                           'Legend\\test artist\\test_album_2\\test_album_2.jpg')
            ),
            SongData(
                file_path=Path('Legend\\test artist\\test_album_2\\4 Name4 (OP1).mp3'),
                title='Name4',
                artist='test artist',
                album='test_album_2',
                feat=[],
                special='(OP1)',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\'
                           'Legend\\test artist\\test_album_2\\test_album_2.jpg')
            ),
            SongData(
                file_path=Path('Legend\\test artist\\test_album_2\\5. Name5 (Just Another Name).mp3'),
                title='Name5',
                artist='test artist',
                album='test_album_2',
                feat=[],
                special='',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\'
                           'Legend\\test artist\\test_album_2\\test_album_2.jpg')
            ),
            SongData(
                file_path=Path('Legend\\test artist\\test_album_2\\6 - +-0.mp3'),
                title='+-0',
                artist='test artist',
                album='test_album_2',
                feat=[],
                special='',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\'
                           'Legend\\test artist\\test_album_2\\test_album_2.jpg')
            ),
            SongData(
                file_path=Path('Legend\\test artist\\test_album_2\\7 +-0.mp3'),
                title='+-0',
                artist='test artist',
                album='test_album_2',
                feat=[],
                special='',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\'
                           'Legend\\test artist\\test_album_2\\test_album_2.jpg')
            ),
            SongData(
                file_path=Path('Legend\\test artist\\test_album_2\\45.mp3'),
                title='45',
                artist='test artist',
                album='test_album_2',
                feat=[],
                special='',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\'
                           'Legend\\test artist\\test_album_2\\test_album_2.jpg')
            ),
            SongData(
                file_path=Path('Legend\\test artist\\test_album_2\\name w-o number.mp3'),
                title='name w-o number',
                artist='test artist',
                album='test_album_2',
                feat=[],
                special='',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\'
                           'Legend\\test artist\\test_album_2\\test_album_2.jpg')
            ),
            SongData(
                file_path=Path('Legend\\test artist\\test_album_2\\6 - +-0.mp3'),
                title='+-0',
                artist='test artist',
                album='test_album_2',
                feat=[],
                special='',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\'
                           'Legend\\test artist\\test_album_2\\test_album_2.jpg')
            ),
            SongData(
                file_path=Path('The Best\\Taio Cruz, Some Artis, Some1 - Dynamite (feat. Some2).mp3'),
                title='Dynamite',
                artist='Taio Cruz',
                album='The Best',
                feat=['Some Artis', 'Some1', 'Some2'],
                special='',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\The Best\\The Best.jpg')
            ),
            SongData(
                file_path=Path('The Best\\test album\\EMPiRE - RiGHT NOW (EN9).mp3'),
                title='RiGHT NOW',
                artist='EMPiRE',
                album='test album',
                feat=[],
                special='(EN9)',
                image=Path('C:\\code\\tag_changer\\test_tag_change\\The Best\\test album\\test album.jpg')
            )
        ]

        for i, file in enumerate(input_data):
            assert tag_changer.get_info_from_file(Path(file)) == output_results[i]

    def test_get_image_and_delete_images(self, tag_changer):
        input_data = [
            (Path('C:\\code\\tag_changer\\test_tag_change\\The Best'), 'The Best'),
            (Path('C:\\code\\tag_changer\\test_tag_change\\The Best\\test album'), 'test album'),
            (Path('C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_1'), 'test_album_1'),
            (Path('C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_2'), 'test_album_2'),
            (Path('C:\\code\\tag_changer\\test_tag_change\\Legend\\Saint Asonia'), 'Saint Asonia'),
        ]
        output_results = [
            None,
            Path('C:\\code\\tag_changer\\test_tag_change\\The Best\\test album\\test album.jpg'),
            None,
            Path('C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_album_2\\test_album_2.jpg'),
            Path('C:\\code\\tag_changer\\test_tag_change\\Legend\\Saint Asonia\\Saint Asonia.jpg'),
        ]
        for i, (file_path, album) in enumerate(input_data):
            assert tag_changer.get_image(file_path, album) == output_results[i]
        tag_changer.delete_images(tag_changer.target_dir)  # TODO дописать тесты через вывод логов
