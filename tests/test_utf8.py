# -*- coding: utf-8 -*-

import sys

import pytest

from asian_word_analyzer.utf8 import _u, _u8

@pytest.mark.skipif(sys.version_info.major < 3, reason="requires python>=3")
@pytest.mark.parametrize('input_string', (b'a', 'a'))
def test__u(input_string):
    assert isinstance(_u(input_string), str)


@pytest.mark.skipif(sys.version_info.major < 3, reason="requires python>=3")
@pytest.mark.parametrize('input_string', (b'a', 'a'))
def test__u8(input_string):
    assert isinstance(_u8(input_string), bytes)    
    
    