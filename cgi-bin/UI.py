#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Wed Apr 22 11:31:22 2015

This file handles the generation of the html code

@author     Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
@version    June 2015
"""

from __future__ import print_function

import sys
import locale                                  # Ensures that subsequent open()s
locale.getpreferredencoding = lambda: 'UTF-8'  # are UTF-8 encoded.


from functools import partial

if sys.version_info.major == 2:
    # guarantee unicode string
    _u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t, str) else t
    _uu = lambda *tt: tuple(_u(t) for t in tt)
    # guarantee byte string in UTF8 encoding
    _u8 = lambda t: t.encode('UTF-8', 'replace') if isinstance(t, unicode) else t
    _uu8 = lambda *tt: tuple(_u8(t) for t in tt)
else:
    # guarantee unicode string
    _u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t, bytes) else t
    _uu = lambda *tt: tuple(_u(t) for t in tt)
    # guarantee byte string in UTF8 encoding
    _u8 = lambda t: t.encode('UTF-8', 'replace') if isinstance(t, str) else t
    _uu8 = lambda *tt: tuple(_u8(t) for t in tt)




if sys.version_info.major == 3:
    utf8stdout = open(1, 'w', encoding='utf-8', closefd=False) # fd 1 is stdout
    utf8print = partial(print , end='\r\n', file=utf8stdout)
elif sys.version_info.major == 2:
    def utf8print(text):
        sys.stdout.write(_u8(text))



# CGI debugging
import cgitb
cgitb.enable()


#==============================================================================
# STANDARD RENDERING FUNCTIONS
#==============================================================================

def render_top(search_box=''):
    utf8print("Content-Type: text/html;  charset=utf8\r\n\n")
    utf8print("")
    utf8print("""<!DOCTYPE html>
<html>
    <!-- Bootstrap core CSS -->
    <link href="../css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="../css/main.css" rel="stylesheet">

    <center>
    <h1> Asian Word Analyzer</h1>
    </center>
    """)


def render_main(word):
    utf8print("""
        <div class="container">
        <center>
        <form name="input" action="/cgi-bin/awa.py" method="get"  accept-charset="utf-8">
        <input type="text" name="word" maxlength="2048" value = '""" +  \
        word.get_string() + """'>
        <input type="submit" value="Go!">
        </form>
        Detected language: """ + word.get_language() + """

        </center>

        <h1 class="page-header">""" + word.get_string() + """</h1>""" + \
        word.get_meaning() + """

        <p>&nbsp;</p>

        <div class="row flat">""")


def render_block(block, words):
    """
    Input:
        - block (column name/header)
        - words (words to be displayed in each column)
    """
    utf8print("""

            <div class="row flat">
            <div class="col-lg-3 col-md-3 col-xs-6">
                <ul class="plan plan1">
                    <li class="plan-name">
                        """ + block.get_string())
    if block.get_ethym():
        utf8print('(' + block.get_ethym() + ')')
    utf8print("""
                    </li> """)

    if block.get_meaning():
        utf8print("""
                    <li class="block-meaning">
                        """ + block.get_meaning() + """
                    </li>""")

    for word in words:
        utf8print("""
                    <li class="plan-price">
                        <strong> <a href="/cgi-bin/awa.py?word=""" + \
                        word.get_string() + """">""" + word.get_string())

        if word.get_ethym():
            utf8print(' (' + word.get_ethym() + ')')

        utf8print("""</a> </strong>&nbsp;&nbsp;""" + word.get_meaning() \
                        +  """
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


#==============================================================================
# SPECIAL RENDERING FUNCTIONS
#==============================================================================

def render_error(error):
    utf8print("<div class='alert-box error'><span>error: </span>" + error + "</div>")
#    utf8print("<b>Error:</b> ")
#    utf8print(error)

#def render_info(info):
#    utf8print("<b>Info:</b> ")
#    utf8print(info)
#    utf8print("<br>")

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

