# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 12:02:49 2016

@author:     Jean-Baptiste Fiot  <jean-baptiste.fiot@centraliens.net>
"""


import pytest

from asian_word_analyzer.korean.word import KoreanWord


@pytest.mark.parametrize('word, expected', ((u'공부하다', u'하다'),
#                                            (u'안녕하세요', u'하세요'),
                                            (u'선생님', u'님')))
def test_compute_suffix(word, expected):
   assert expected == KoreanWord(word).suffix
   
   