import pytest
from tag_changer import TagChanger


@pytest.fixture(scope="class")
def tag_changer():
    return TagChanger('a', ['a', 'b'])


class TestClass:
    def test_find_numbers_with_artist(self, tag_changer):
        assert tag_changer.find_numbers('12. Artist - Title') == 'Artist - Title'
        assert tag_changer.find_numbers('12) Artist - Title') == 'Artist - Title'
        assert tag_changer.find_numbers('12)Artist - Title') == 'Artist - Title'
        assert tag_changer.find_numbers('12 - Artist - Title') == 'Artist - Title'
        assert tag_changer.find_numbers('12- Artist - Title') == 'Artist - Title'
        assert tag_changer.find_numbers('12 -Artist - Title') == '-Artist - Title'
        assert tag_changer.find_numbers('12Artist - Title') == '12Artist - Title'
        assert tag_changer.find_numbers('Sum41 - Title') == 'Sum41 - Title'
        assert tag_changer.find_numbers('Sum 41 - Title') == 'Sum 41 - Title'
        assert tag_changer.find_numbers('41 Sum 41 - 41') == 'Sum 41 - 41'
        assert tag_changer.find_numbers('41) Sum 41 - 41') == 'Sum 41 - 41'
        assert tag_changer.find_numbers('41 - Sum 41 - 41') == 'Sum 41 - 41'

    def test_find_numbers_without_artist(self, tag_changer):
        assert tag_changer.find_numbers('1. Title') == 'Title'
        assert tag_changer.find_numbers('1)Title') == 'Title'
        assert tag_changer.find_numbers('1) Title') == 'Title'
        assert tag_changer.find_numbers('1 - Title') == 'Title'
        assert tag_changer.find_numbers('1- Title') == 'Title'
        assert tag_changer.find_numbers('1 -Title') == '-Title'
        assert tag_changer.find_numbers('1) +-') == '+-'
        assert tag_changer.find_numbers('1. +-') == '+-'
        assert tag_changer.find_numbers('1 - +-') == '+-'
        assert tag_changer.find_numbers('1- +-') == '+-'
        assert tag_changer.find_numbers('1)+-') == '+-'
        assert tag_changer.find_numbers('Sum 41') == 'Sum 41'
        assert tag_changer.find_numbers('Sum41') == 'Sum41'
        assert tag_changer.find_numbers('41Sum') == '41Sum'
        assert tag_changer.find_numbers('41) 41') == '41'
        assert tag_changer.find_numbers('41. 41') == '41'
        assert tag_changer.find_numbers('41 - 41') == '41'
        assert tag_changer.find_numbers('41- 41') == '41'
        assert tag_changer.find_numbers('name w-o number') == 'name w-o number'
        assert tag_changer.find_numbers('name w - o number') == 'name w - o number'

    def test_find_numbers_special(self, tag_changer):
        # TODO не уверен правильно ли это
        assert tag_changer.find_numbers('41 Sum') == 'Sum'
        assert tag_changer.find_numbers('12.Artist - Title') == '12.Artist - Title'
        assert tag_changer.find_numbers('12 Artist - Title') == 'Artist - Title'

    def test_split_artist(self, tag_changer):
        assert tag_changer.split_artist('Artist, Other2, Other3') == ('Artist', ['Other2', 'Other3'])
        assert tag_changer.split_artist('Artist,Other2,Other3') == ('Artist', ['Other2', 'Other3'])

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
        assert tag_changer.find_anime('Title (EN One Piece)') == ('Title', '(EN One Piece)')
        assert tag_changer.find_anime('Title (OP One Piece)') == ('Title', '(OP One Piece)')
        assert tag_changer.find_anime('Title (OPOne Piece)') == ('Title (OPOne Piece)', '')
        assert tag_changer.find_anime('Title (OP 1)') == ('Title', '(OP 1)')
        assert tag_changer.find_anime('Title (EN 1)') == ('Title', '(EN 1)')
        assert tag_changer.find_anime('Title (OP1)') == ('Title', '(OP1)')
        assert tag_changer.find_anime('Title (EN1)') == ('Title', '(EN1)')
        # self.assertEqual((['Artist', 'Title (EN One Piece)'], 'Title (EN One Piece)'), prepare_name(Path('Artist - Title (EN One Piece).mp3')))
        # self.assertEqual((['Artist', 'Title (OP One Piece)'], 'Title (OP One Piece)'), prepare_name(Path('Artist - Title (OP One Piece).mp3')))
        # self.assertEqual((['Artist', 'Title'], 'Title'), prepare_name(Path('Artist - Title (OPOne Piece).mp3')))
        # self.assertEqual((['Artist', 'Title (OP 1)'], 'Title (OP 1)'), prepare_name(Path('Artist - Title (OP 1).mp3')))
        # self.assertEqual((['Artist', 'Title (OP1)'], 'Title (OP1)'), prepare_name(Path('Artist - Title (OP1).mp3')))

    def test_split_fullname(self, tag_changer):
        assert tag_changer.split_fullname('Artist - Title') == ('Artist', 'Title')
        assert tag_changer.split_fullname('Artist - Titleft (feat. Man)') == ('Artist', 'Titleft (feat. Man)')
        assert tag_changer.split_fullname('Artist - Title (OP One Piece)') == ('Artist', 'Title (OP One Piece)')
        assert tag_changer.split_fullname('Title') == ('', 'Title')
        assert tag_changer.split_fullname('name w - o number') == ('name w', 'o number')



    # def test_prepare_name(self) -> None:
    #     print('test prepare_name()')
    #
    #     self.assertEqual((['Artist', 'Title'], 'Title'), prepare_name(Path('Artist - Title.mp3')))
    #     self.assertEqual((['Artist', 'Title'], 'Title'), prepare_name(Path('Artist - Title (New edition).mp3')))
    #     self.assertEqual((['Artist', 'Titleft (feat. Man)'], 'Titleft (feat. Man)'), prepare_name(Path('Artist - Titleft (feat. Man).mp3')))
    #     self.assertEqual((['Artist', 'Title (ft. Man)'], 'Title (ft. Man)'), prepare_name(Path('Artist - Title (ft. Man).mp3')))
    #     self.assertEqual((['Artist', 'Title(feat. Man)'], 'Title(feat. Man)'), prepare_name(Path('Artist - Title(feat. Man).mp3')))
    #     self.assertEqual((['Artist', 'Title'], 'Title'), prepare_name(Path('Artist - Title(New edition).mp3')))
    #     self.assertEqual((['Artist', 'Title'], 'Title'), prepare_name(Path('Artist - Title(featmen).mp3')))
    #     self.assertEqual((['Artist', 'Title'], 'Title'), prepare_name(Path('Artist - Title(FeatMen).mp3')))
    #     self.assertEqual((['Artist', 'The (S)hift'], 'The (S)hift'), prepare_name(Path('Artist - The (S)hift.mp3')))
    #     self.assertEqual((['Artist', 'The Sh(i)ft'], 'The Sh(i)ft'), prepare_name(Path('Artist - The Sh(i)ft.mp3')))
    #
    #     self.assertEqual(('Title (feat. Artist1, Artis2, Artis3)', 'Artist'), change_feat('Title (feat. Artist1)', 'Artist, Artis2, Artis3'))
    #     self.assertEqual(('Titleft ftdoc (feat. Man)', 'Artist'), change_feat('Titleft ftdoc', 'Artist, Man'))
    #     self.assertEqual(('Titleft (ftdoc) (feat. Dave)', 'Artist'), change_feat('Titleft (ftdoc)', 'Artist,Dave'))

    # @unittest.skip("special cases")
    # def test_prepare_name_special(self) -> None:
    #     print('special test prepare_name()')
    #
    #     self.assertEqual((['Sum'], 'Sum'), prepare_name(Path('41 Sum.mp3')))
    #     # TODO не уверен правильно ли это
    #     self.assertEqual((['12.Artist', 'Title'], 'Title'), prepare_name(Path('12.Artist - Title.mp3')))
    #     self.assertEqual((['Artist', 'Title'], 'Title'), prepare_name(Path('12 Artist - Title.mp3')))
