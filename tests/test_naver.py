# -*- coding: utf-8 -*-

from asian_word_analyzer.korean.naver import get_hanja


def test_get_hanja():
    assert u'安寧' == get_hanja(u'안녕') 