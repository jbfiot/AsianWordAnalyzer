#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Wed Apr 22 11:31:22 2015

This file handles the generation of the html code

@author     Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
"""

from __future__ import print_function

from functools import partial
import locale

import cgitb

# Ensures that subsequent open()s are UTF-8 encoded.
locale.getpreferredencoding = lambda: 'UTF-8'

utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)  # fd 1 is stdout
utf8print = partial(print, end='\r\n', file=utf8stdout)

cgitb.enable()


# ==============================================================================
#                    STANDARD RENDERING FUNCTIONS
# ==============================================================================

def render_top():
    utf8print("Content-Type: text/html;  charset=utf8\r\n\n")
    utf8print("")
    utf8print("""<!DOCTYPE html>
<html>
    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="css/main.css" rel="stylesheet">

    <center>
    <h1> Asian Word Analyzer</h1>
    </center>
    
    <div class="container">

    """)


def render_main(word):
    if word.ethym:
        ethym_str = ' ({})'.format(word.ethym)
    else:
        ethym_str = ''
    if word.language:
        language_str = 'Detected language: {}'.format(word.language)
    else:
        language_str = ''
    utf8print("""
        <center>
        <form name="input" action="/awa.py" method="get"  accept-charset="utf-8">
        <input type="text" name="word" maxlength="2048" value = '""" + word.string + """'>
        <input type="submit" value="Go!">
        </form>
        """ + language_str + """

        </center>

        <h1 class="page-header">""" + word.string + ethym_str + """</h1>""" + word.meaning + """

        <p>&nbsp;</p>

        <div class="row flat">""")


def render_block(block, words):
    """
    Input:
        - block (column name/header)
        - words (words to be displayed in each column)
    """
    utf8print("""

            <div class="col-lg-3 col-md-3 col-xs-6">
                <ul class="plan plan1">
                    <li class="plan-name">
                        """ + block.string)
    if block.ethym:
        utf8print('(' + block.ethym + ')')
    utf8print("""
                    </li> """)

    if block.name:
        utf8print("""
                    <li class="block-name">
                        """ + block.name + """
                    </li>""")

    if block.meaning:
        utf8print("""
                    <li class="block-meaning">
                        """ + block.meaning + """
                    </li>""")

    for word_idx in range(len(words)):
        word = words.ix[word_idx]
        utf8print("""
                    <li class="plan-price">
                        <strong> <a href="/awa.py?word=""" + word.word + """">""" + word.word)

        if word.ethym:
            utf8print(' (' + word.ethym + ')')

        utf8print("""</a> </strong>&nbsp;&nbsp;""" + word.meaning + """
                    </li>""")
    utf8print("""
                </ul>
            </div>

    """)


def render_bottom():
    utf8print("""      
        </div>
    </div> <!-- /container -->
</html>""")


# ==============================================================================
#                      SPECIAL RENDERING FUNCTIONS
# ==============================================================================

def render_error(error):
    utf8print("<div class='alert-box error'><span>error: </span>" + error + "</div>")


def render_info(info):
    utf8print("<div class='alert-box notice'><span>info: </span>" + info + "</div>")


def render_empty():
    utf8print("Content-Type: text/html;  charset=utf8; \r\n\n")
    utf8print("")
    utf8print("""<!DOCTYPE html>
    <html>
    Empty Page
    </html>
    """)

