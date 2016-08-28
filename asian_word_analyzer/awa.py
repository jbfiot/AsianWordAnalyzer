#!/usr/bin/python
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Wed Apr 22 11:31:22 2015

This file is the main CGI script for the AsianWordAnalyzer.


@author     Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
"""

import sys
import cgi
#import cgitb

from asian_word_analyzer.utf8 import _u
import asian_word_analyzer.UI as UI
from asian_word_analyzer.tools import detect_language


#cgitb.enable()
DEBUG = False


#UI.render_empty()

# Entree
UI.render_top()

if DEBUG:
    UI.render_info('Python version ' + str(sys.version_info.major))


# Main
form = cgi.FieldStorage()
if 'word' in form.keys():
    input_str = form["word"].value
    try:    
        language = detect_language(_u(input_str))
    except ValueError:
        UI.render_error('Language not supported')
        

    if language == 'korean':
        from asian_word_analyzer.korean.db import get_words_with_block
        from asian_word_analyzer.korean.word import KoreanWord as Word
    elif language == 'thai':
        from asian_word_analyzer.thai.Thai import get_words_with_block
        from asian_word_analyzer.thai.Thai import ThaiWord as Word

    if 'Word' in locals():
        word = Word(input_str, compute_ethym=True)
        UI.render_main(word)
        blocks = word.get_blocks_for_selected_meaning()
        for block in blocks:
            words = get_words_with_block(block, exclude=word)
            UI.render_block(block, words)
else:
    from EmptyWord import EmptyWord
    UI.render_main(EmptyWord())

# Desert
UI.render_bottom()

