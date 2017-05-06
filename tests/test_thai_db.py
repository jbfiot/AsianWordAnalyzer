# -*- coding: utf-8 -*-

from asian_word_analyzer.thai.db import DbUtil


class TestDbUtil:
    def test_compute_meanings(self):
        util = DbUtil()
        assert 'paper' in util.compute_meanings(u'กระดาษ').values
