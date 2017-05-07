#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Wed Apr 22 11:31:22 2015

This file is the main CGI script for the AsianWordAnalyzer.


@author     Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
"""

import sys
import cgi
import cgitb

sys.path.append('..')  # TODO: investigate cleaner solution

from asian_word_analyzer.utf8 import _u
import asian_word_analyzer.ui as UI
from asian_word_analyzer.tools import detect_language
from asian_word_analyzer.korean.db import DbUtil as KoreanDbUtil
from asian_word_analyzer.korean.word import KoreanWord
from asian_word_analyzer.thai.db import DbUtil as ThaiDbUtil
from asian_word_analyzer.thai.word import ThaiWord
from asian_word_analyzer.empty_word import EmptyWord

#cgitb.enable()


def get_word_and_db_util_classes(language):
    if language == 'korean':
        return KoreanDbUtil, KoreanWord
    elif language == 'thai':
        return ThaiDbUtil, ThaiWord

# Entree
UI.render_top()

# Main
form = cgi.FieldStorage()
if 'word' in form.keys():
    input_str = form["word"].value
    try:    
        language = detect_language(_u(input_str))
    except ValueError:
        UI.render_error('Language not supported')

    if 'language' in locals():
        DbUtil, Word = get_word_and_db_util_classes(language)
        word = Word(input_str, compute_etymology=True)
        UI.render_main(word)
        blocks = word.get_blocks_for_selected_meaning()
        for block in blocks:
            words = DbUtil().get_words_with_block(block, exclude=word)
            UI.render_block(block, words)
else:
    UI.render_main(EmptyWord())

# Desert
UI.render_bottom()

