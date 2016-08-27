# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 09:24:16 2016

@author: jbfiot
"""

import pytest

from asian_word_analyzer.tools import detect_language


@pytest.mark.parametrize('word, expected',
                         ((u'안녕하세요', 'korean'), 
                          (u'เป็นได้ ', 'thai') 
                         ))
def test_detect_language(word, expected):
    assert expected == detect_language(word)
    
    
@pytest.mark.parametrize('word', (u'مرحبا', u'Χαίρετε'))
def test_detect_language_failure(word):
    with pytest.raises(ValueError):
        detect_language(word)
    