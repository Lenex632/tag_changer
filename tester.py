import unittest
from tag_changer import *


class TestMain(unittest.TestCase):
    def test_feat_changer(self) -> None:
        print('test feat_changer()')

        self.assertEqual(('Titleft ftdoc (feat. Man)', 'Artist'), change_feat('Titleft ftdoc', 'Artist, Man'))
        self.assertEqual(('Titleft (ftdoc) (feat. Dave)', 'Artist'), change_feat('Titleft (ftdoc)', 'Artist,Dave'))

        self.assertEqual(('Titleft featdoc', 'Artist'), change_feat('Titleft featdoc', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft ft doc', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft feat doc', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft ft. doc', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft ft.doc', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft feat. doc', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft feat.doc', 'Artist'))

        self.assertEqual(('Titleft(featdoc)', 'Artist'), change_feat('Titleft(featdoc)', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft (ft doc)', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft(feat doc)', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft(feat doc)', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft (feat doc)', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft (ft. doc)', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft (ft.doc)', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'ftDog'), change_feat('Titleft (ft.doc)', 'ftDog'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft (feat.doc)', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft (feat. doc)', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft(feat. doc)', 'Artist'))
        self.assertEqual(('Titleft (feat. doc)', 'Artist'), change_feat('Titleft(feat.doc)', 'Artist'))

    def test_prepare_name(self) -> None:
        print('test prepare_name()')

        self.assertEqual(['Artist', 'Title'], prepare_name(Path('Artist - Title.mp3')))
        self.assertEqual(['Artist', 'Title'], prepare_name(Path('Artist - Title (New edition).mp3')))
        self.assertEqual(['Artist', 'Titleft (feat. Man)'], prepare_name(Path('Artist - Titleft (feat. Man).mp3')))
        self.assertEqual(['Artist', 'Title (ft. Man)'], prepare_name(Path('Artist - Title (ft. Man).mp3')))
        self.assertEqual(['Artist', 'Title(feat. Man)'], prepare_name(Path('Artist - Title(feat. Man).mp3')))
        self.assertEqual(['Artist', 'Title'], prepare_name(Path('Artist - Title(New edition).mp3')))
        self.assertEqual(['Artist', 'Title'], prepare_name(Path('Artist - Title(featmen).mp3')))
        self.assertEqual(['Artist', 'Title'], prepare_name(Path('Artist - Title(FeatMen).mp3')))
        self.assertEqual(['Artist', 'Title (EN One Piece)'], prepare_name(Path('Artist - Title (EN One Piece).mp3')))
        self.assertEqual(['Artist', 'Title (OP One Piece)'], prepare_name(Path('Artist - Title (OP One Piece).mp3')))
        self.assertEqual(['Artist', 'The (S)hift'], prepare_name(Path('Artist - The (S)hift.mp3')))
        self.assertEqual(['Artist', 'The Sh(i)ft'], prepare_name(Path('Artist - The Sh(i)ft.mp3')))

        self.assertEqual(['Artist', 'Title'], prepare_name(Path('12. Artist - Title.mp3')))
        self.assertEqual(['Artist', 'Title'], prepare_name(Path('12) Artist - Title.mp3')))
        self.assertEqual(['Artist', 'Title'], prepare_name(Path('12)Artist - Title.mp3')))
        self.assertEqual(['Artist', 'Title'], prepare_name(Path('12 - Artist - Title.mp3')))
        self.assertEqual(['Artist', 'Title'], prepare_name(Path('12- Artist - Title.mp3')))
        self.assertEqual(['-Artist', 'Title'], prepare_name(Path('12 -Artist - Title.mp3')))
        self.assertEqual(['12Artist', 'Title'], prepare_name(Path('12Artist - Title.mp3')))
        self.assertEqual(['Sum41', 'Title'], prepare_name(Path('Sum41 - Title.mp3')))
        self.assertEqual(['Sum 41', 'Title'], prepare_name(Path('Sum 41 - Title.mp3')))

        self.assertEqual(['Title'], prepare_name(Path('1. Title.mp3')))
        self.assertEqual(['Title'], prepare_name(Path('1)Title.mp3')))
        self.assertEqual(['Title'], prepare_name(Path('1) Title.mp3')))
        self.assertEqual(['Title'], prepare_name(Path('1 - Title.mp3')))
        self.assertEqual(['Title'], prepare_name(Path('1- Title.mp3')))
        self.assertEqual(['-Title'], prepare_name(Path('1 -Title.mp3')))
        self.assertEqual(['+-'], prepare_name(Path('1) +-.mp3')))
        self.assertEqual(['+-'], prepare_name(Path('1. +-.mp3')))
        self.assertEqual(['+-'], prepare_name(Path('1 - +-.mp3')))
        self.assertEqual(['+-'], prepare_name(Path('1- +-.mp3')))
        self.assertEqual(['+-'], prepare_name(Path('1)+-.mp3')))
        self.assertEqual(['Sum 41'], prepare_name(Path('Sum 41.mp3')))
        self.assertEqual(['Sum41'], prepare_name(Path('Sum41.mp3')))
        self.assertEqual(['41Sum'], prepare_name(Path('41Sum.mp3')))
        self.assertEqual(['41'], prepare_name(Path('41) 41.mp3')))
        self.assertEqual(['41'], prepare_name(Path('41. 41.mp3')))
        self.assertEqual(['41'], prepare_name(Path('41 - 41.mp3')))
        self.assertEqual(['41'], prepare_name(Path('41- 41.mp3')))

        self.assertEqual(['Sum 41', '41'], prepare_name(Path('41 Sum 41 - 41.mp3')))
        self.assertEqual(['Sum 41', '41'], prepare_name(Path('41) Sum 41 - 41.mp3')))
        self.assertEqual(['Sum 41', '41'], prepare_name(Path('41 - Sum 41 - 41.mp3')))

    @unittest.skip
    def special_test_prepare_name(self) -> None:
        print('special test prepare_name()')

        self.assertEqual(['Sum'], prepare_name(Path('41 Sum.mp3')))
        self.assertEqual(['12.Artist', 'Title'], prepare_name(Path('12.Artist - Title.mp3')))  # TODO не уверен правильно ли
        self.assertEqual(['Artist', 'Title'], prepare_name(Path('12 Artist - Title.mp3')))


if __name__ == '__main__':
    unittest.main()
