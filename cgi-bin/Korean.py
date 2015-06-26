#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Wed Apr 22 11:31:22 2015

@author:    Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
@version:   June 2015
"""


#==============================================================================
# MODULES
#==============================================================================


import sys

# CGI debugging
import cgitb
cgitb.enable()
DEBUG = 0

# AWA components
from Block import Block
import UI
import login
import tools

# Web requests
if sys.version_info.major == 2:
    import urllib2
else:
    import urllib


from bs4 import BeautifulSoup

import pandas as pd
from sqlalchemy import create_engine


import codecs # for opening files in python2 with UTF8 encoding

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


# Method
METHOD = 'db' # available methods: 'dic', 'db'

# Dictionnary
#FILE = '/home/jbfiot/www/cgi-bin/data/mini.txt'
FILE = '/home/jbfiot/www/data/korean2.txt'


#==============================================================================
# LANGUAGE METHODS
#==============================================================================

def get_words_with_block(block, exclude=None):
    """
    This functions returns a list of Korean words that rely on the same block.
    """

    # DICTIONNARY IMPLEMENTATION
    if METHOD == 'dic':
        f = codecs.open(FILE, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        words = []
        for line in lines:
            # Implementation 1: using hangul syllables
            if block.get_string() in line.split(',')[0]:
                word = line.split(',')[0].strip()
                if word != exclude:
                    words.append(KoreanWord(string=word, \
                                            meaning=line.split(',')[1].strip()))


    # DATABASE IMPLEMENTATION
    if METHOD == 'db':
        if block.get_ethym():
            query = """SELECT * FROM `Korean` WHERE INSTR( ethym, '""" + block.get_ethym() + """') >0"""
            engine = create_engine(login.connection_string, echo=False)
            results = pd.io.sql.execute(query, engine)
            results = results.fetchall()
            words = [KoreanWord(string=r[0], ethym=r[1], meaning=r[2]) \
                        for r in results if r[0] != exclude and \
                        len(r[0]) == len(r[1]) and tools.detect_language(r[1]) is not 'korean']
                        # len check and ethym check to avoid some corrupted data from the database to be displayed
        else:
            # For example, we do not return a list of words for suffixes
            words = []

    return words




class KoreanWord(object):
    """ This class is used to manipulate Korean words. """
    def __init__(self, string='', ethym=None, meaning=None, compute_ethym=False):
        self.string = _u(string)  # e.g. user input string
        self.language = 'Korean'

        if ethym and meaning:
            self.blocks = [[Block(string[i], ethym=ethym[i]) for i in range(len(string))]] # assuming hangul and hanja have the same length
            self.meanings = [meaning]
            self.selected_meaning = 0 # the word is clearly defined

        else:
            self.blocks = self.compute_blocks(compute_ethym)
            self.meanings = self.compute_meanings() # Different meanings in English
            self.selected_meaning = 0 # index of the selected meaning



    #==========================================================================
    #  GETTERS
    #==========================================================================

    def get_string(self):
        """ String getter """
        return self.string

    def get_language(self):
        """ Language getter """
        return self.language

    def get_blocks(self):
        """ Blocks getter """
        return self.blocks

    def get_meaning(self):
        """ Meaning getter """
        return self.meanings[self.selected_meaning]

    def get_blocks_for_selected_meaning(self):
        """ Getter for the blocks corresponding to the selected meaning """
        return self.blocks[self.selected_meaning]

    def get_ethym(self):
        return ''.join([block.get_ethym() for block in \
                    self.blocks[self.selected_meaning] if block.get_ethym()])

    #==========================================================================
    #  PRINT METHODS
    #==========================================================================

    def print_blocks_for_selected_meaning(self):
        """ This methods prints the block strings for the selected meaning.

        Example:
        --------
            For the word '안녕', the blocks will be ['안', '녕']
        """
        return [block.get_str() for block in self.blocks[self.selected_meaning]]


    #==========================================================================
    #   LANGUAGE METHODS
    #==========================================================================

    def compute_meanings(self):
        """ Find the meaning.
        Note:
        """
        f = codecs.open(FILE, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        for line in lines:
            if line.split(',')[0].strip() == self.string:
                return [line.split(',')[1].strip()]
        return ['']


    def compute_blocks(self, compute_ethym=False):
        """ Compute the blocks given the input string.

        Output:
            Returns a list of lists of blocks, i.e.
            [ [b11, ..., b1n1], [b21, ..., b2n2], ...], where each list of
            blocks [bi1, ..., bini] corresponds to a possible meaning of the
            input string.

        Note:
            In this CSV dictionnary based implemenation, only one meaning is
            available.
        """
        if DEBUG:
            UI.render_info('compute_blocks() called for word ' + self.string)

        suffixes = {u'하다':u'하다 verb particule', \
            u'합니다': u'formal 하다 ending', \
            u'하세요': u'formal imperative form of 하다', \
              u'요': u'politeness particle'}

        detected_suffix = ''
        for suffix in suffixes.keys():
            if self.string.endswith(suffix):
                detected_suffix = suffix
                continue
        body = self.string[0:len(self.string)-len(detected_suffix)]

        if not compute_ethym:
            blocks = [Block(body[i]) for i in range(len(body)) if body[i] != ' ']
        else:
            ethym = get_hanja(body)
            if DEBUG:
                UI.render_info(ethym)
            blocks = [Block(body[i], ethym=ethym[i], \
                        meaning=get_hanja_meaning(ethym[i])) \
                        for i in range(len(body)) if body[i] != ' ']

        if detected_suffix:
            suffix_desc = 'Suffix: ' + suffixes[detected_suffix]
            blocks.append(Block(detected_suffix, meaning=suffix_desc))

        return [blocks]



# EXPERIMENTAL


def get_hanja_meaning(hanja):
    query = "SELECT meaning from Korean_ethym WHERE ethym='" + hanja + "'"
    engine = create_engine(login.connection_string, echo=False)
    results = pd.io.sql.execute(query, engine)
    results = results.fetchall()
    if results:
        return results[0][0]
    else:
        return None



def get_hanja(hangul):

    if sys.version_info.major == 2: # Python 2
        search = ''.join('%' + format(ord(a), 'x') for a in hangul.encode('utf8'))
    elif sys.version_info.major == 3: # Python 3
        search = ''.join('%' + "{:02x}".format(a) for a in hangul.encode('utf8'))


#    url = u"http://hanja.naver.com/search?query=휴업" # not supported by urllib
    url='http://hanja.naver.com/search?query=' + search
    url='http://endic.naver.com/search.nhn?sLn=kr&query=' + search


    if sys.version_info.major == 2:
        contents = urllib2.urlopen(url)
        contents = contents.read()
    else:
        contents = urllib.request.urlopen(url).read() #Python 3
        contents.decode('utf8')



    soup = BeautifulSoup(contents)
    first = soup.find('dt', {'class':'first'})
    strings = [s for s in first.stripped_strings]
    hanja = strings[-1]

    if hanja is not '.':
        return hanja
    else:
        return None