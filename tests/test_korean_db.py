# -*- coding: utf-8 -*-

import pytest

from asian_word_analyzer.korean.db import DbUtil
from asian_word_analyzer.korean.word import KoreanWord


class TestDbUtil:

    def test_no_db(self, monkeypatch):
        monkeypatch.setattr('asian_word_analyzer.korean.db.connection_string', 'dummy')
        with pytest.raises(FileNotFoundError):
            DbUtil()

    @pytest.mark.parametrize('hanja, expected',
                             [
                                 [u'大', u'클 대 / 큰 대'],
                                 ['dummy', None]
                             ])
    def test_get_hanja_name(self, hanja, expected):
        util = DbUtil()
        assert expected == util.get_hanja_name(hanja)

    @pytest.mark.parametrize('hanja, expected',
                             [
                                 [u'大', 'big'],
                                 ['dummy', None]
                             ])
    def test_get_hanja_meaning(self, hanja, expected):
        util = DbUtil()
        assert expected == util.get_hanja_meaning(hanja)

    def test_compute_meanings(self):
        util = DbUtil()
        assert '(평안) (public) peace (안정) stability, well' in util.compute_meanings(u'안녕')

    @pytest.mark.parametrize('input_str, exclude, input_str_expected',
                             [
                                 [u'안녕', None, True],
                                 [u'안녕', u'안녕', False],
                             ])
    def test_get_words_with_block(self, input_str, exclude, input_str_expected):
        word = KoreanWord(input_str, compute_etymology=True)
        block = word.get_blocks_for_selected_meaning()[0]
        words = DbUtil().get_words_with_block(block, exclude=exclude)
        assert len(words) > 0
        assert input_str_expected == (input_str in [word[0] for word in words])
