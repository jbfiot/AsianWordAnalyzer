#!/usr/bin/python
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Wed Apr 22 11:31:22 2015

This file is the main CGI script for the AsianWordAnalyzer.


@author     Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
@version    June 2015
"""


#==============================================================================
# MODULES
#==============================================================================


# CGI and CGI debugging
import cgi
import cgitb
#cgitb.enable()

# AWA components
import UI
from tools import detect_language

import sys

from asian_word_analyzer.utf8 import _u


DEBUG = False

#==============================================================================
# AWA MAIN
#==============================================================================

#UI.render_empty()

# Entree
UI.render_top()

if DEBUG:
    UI.render_info('Python version ' + str(sys.version_info.major))


# Main
form = cgi.FieldStorage()
if 'word' in form.keys():
    input_str = form["word"].value
    language = detect_language(_u(input_str))
    if DEBUG:
        UI.render_info(language)


    if language == 'korean':
        from Korean import get_words_with_block
        from Korean import KoreanWord as Word
    elif language == 'thai':
        from Thai import get_words_with_block
        from Thai import ThaiWord as Word
    else:
        UI.render_error('Language not supported')

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

