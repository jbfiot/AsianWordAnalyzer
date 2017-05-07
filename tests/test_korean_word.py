# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 12:02:49 2016

@author:     Jean-Baptiste Fiot  <jean-baptiste.fiot@centraliens.net>
"""


import pytest

from asian_word_analyzer.korean.word import KoreanWord


class TestKoreanWord:
    
    @pytest.mark.parametrize('string, etymology, meaning',
                             [
                                 [u'안녕', u'安寧', None],
                                 [u'남대문', u'南大門',
                                  u'(건축물) Namdaemun, the (Great) South Gate (of Seoul)']
                             ])
    def test_init(self, string, etymology, meaning):
        KoreanWord(string, etymology, meaning)
    
    def test_init_incorrect_etymology(self):
        with pytest.raises(ValueError):
            KoreanWord(u'안녕', etymology=u'安寧安寧')

    @pytest.mark.parametrize('word, expected', ((u'공부하다', u'하다'),
                                                # (u'안녕하세요', u'하세요'),
                                                (u'선생님', u'님')))
    def test_compute_suffix(self, word, expected):
        assert expected == KoreanWord(word).suffix
