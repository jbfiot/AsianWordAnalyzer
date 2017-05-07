# -*- coding: utf-8 -*-

import pytest

from asian_word_analyzer.korean.db import DbUtil
from asian_word_analyzer.korean.word import KoreanWord


class TestDbUtil:

    def test_no_db(self, monkeypatch):
        monkeypatch.setattr('asian_word_analyzer.korean.db.connection_string', 'dummy')
        with pytest.raises(FileNotFoundError):
            DbUtil()

    def test_get_hanja_name(self):
        util = DbUtil()
        assert u'클 대 / 큰 대' == util.get_hanja_name(u'大')

    def test_get_hanja_meaning(self):
        util = DbUtil()
        assert 'big' == util.get_hanja_meaning(u'大')

    def test_compute_meanings(self):
        util = DbUtil()
        assert '(평안) (public) peace (안정) stability, well' in util.compute_meanings(u'안녕').values

    def test_get_words_with_block(self):
        input_str = u'안녕'
        word = KoreanWord(input_str, compute_etymology=True)
        block = word.get_blocks_for_selected_meaning()[0]
        words = DbUtil().get_words_with_block(block)
        assert len(words) > 0
        assert input_str in words.word.values
