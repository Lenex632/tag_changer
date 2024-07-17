from pathlib import Path

import pytest
from tag_changer import TagChanger
from logger import set_up_logger_config


@pytest.fixture(scope="class")
def tag_changer():
    return TagChanger('a', ['a', 'b'])


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
        files = [
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\Saint Asonia\\Saint Asonia,Sharon den Adel - Sirens.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_albom_2\\1. Name1.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_albom_2\\2 - Name2 (feat. artist).mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_albom_2\\3 Name3 (Japen Version).mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_albom_2\\4 Name4 (OP1).mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_albom_2\\5. Name5 (Just Anothe Name).mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_albom_2\\6 - +-0.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_albom_2\\7 +-0.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_albom_2\\45.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_albom_2\\name w-o number.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\Legend\\test artist\\test_albom_2\\6 - +-0.mp3',
            'C:\\code\\tag_changer\\test_tag_change\\The Best\\Taio Cruz, Some Artis, Some2 - Dynamite (feat. Some1).mp3',
            'C:\\code\\tag_changer\\test_tag_change\\The Best\\test album\\EMPiRE - RiGHT NOW (EN9).mp3'
        ]
        results = [
            ('Saint Asonia', 'Sirens', ['Sharon den Adel'], ''),
            ('', 'Name1', [], ''),
            ('', 'Name2', ['artist'], ''),
            ('', 'Name3', [], ''),
            ('', 'Name4', [], '(OP1)'),
            ('', 'Name5', [], ''),
            ('', '+-0', [], ''),
            ('', '+-0', [], ''),
            ('', '45', [], ''),
            ('', 'name w-o number', [], ''),
            ('', '+-0', [], ''),
            ('Taio Cruz', 'Dynamite', ['Some Artis', 'Some2', 'Some1'], ''),
            ('EMPiRE', 'RiGHT NOW', [], '(EN9)')
        ]

        for i, file in enumerate(files):
            assert tag_changer.get_info_from_file(Path(file)) == results[i]
