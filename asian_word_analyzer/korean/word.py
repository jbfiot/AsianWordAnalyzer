#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Wed Apr 22 11:31:22 2015

@author:    Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
"""


#==============================================================================
# MODULES
#==============================================================================

# CGI debugging
import cgitb
cgitb.enable()
DEBUG = False

# AWA components
from Block import Block
import UI
import login
import tools

# For interacting with the database
from sqlalchemy import create_engine
import pandas as pd


from asian_word_analyzer.utf8 import _u
from asian_word_analyzer.korean.naver import get_hanja


#==============================================================================
# KoreanWord CLASS
#==============================================================================

class KoreanWord(object):
    """ This class is used to manipulate Korean words. """
    def __init__(self, string='', ethym=None, meaning=None, compute_ethym=False):
        self.string = _u(string)  # e.g. user input string
        self.language = 'Korean'

        if ethym and meaning:
            assert(len(string) == len(ethym)) # to the best of my knowledge a
                                              # Korean word and its hanja
                                              # representation (when existing)
                                              # have the same lengths
            self.blocks = [[Block(string[i], ethym=ethym[i]) for i in range(len(string))]]
            self.meanings = [meaning]
            self.selected_meaning = 0 # the word is clearly defined

        else:
            self.compute_suffix()
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
            For the word '안녕', the printed blocks will be ['안', '녕']
        """
        return [block.get_str() for block in self.blocks[self.selected_meaning]]


    #==========================================================================
    #   LANGUAGE METHODS
    #==========================================================================

    def compute_suffix(self):
        """ This method computes:
        self.suffix
        self.suffix_meaning
        self.string_without_suffix
        """
        suffixes = {u'하다':u'하다 verb particule', \
                    u'합니다': u'formal 하다 ending', \
                    u'하세요': u'formal imperative form of 하다', \
                    u'요': u'politeness particle',\
                    u'님': u'honorific particle'}
        # TODO: store the suffixes in the database instead of hardcoding them here

        detected_suffix = ''
        for suffix in suffixes.keys():
            if self.string.endswith(suffix):
                detected_suffix = suffix
                continue
        self.string_without_suffix = self.string[0:len(self.string)-len(detected_suffix)]
        self.suffix = detected_suffix

        if detected_suffix:
            self.suffix_meaning = suffixes[detected_suffix]
        else:
            self.suffix_meaning = None




    def compute_meanings(self):
        """ Find the possible meanings based on the input string by the user"""
        query = "SELECT meaning from Korean WHERE word='" + \
                                               self.string_without_suffix + "'"
        engine = create_engine(login.connection_string, echo=False)
        results = pd.io.sql.execute(query, engine)
        results = results.fetchall()
        if results:
            return results[0]
        else:
            return ['']



    def compute_blocks(self, compute_ethym=False):
        """ Compute the blocks given the input string.

        Output:
            Returns a list of lists of blocks, i.e.
            [ [b11, ..., b1n1], [b21, ..., b2n2], ...], where each list of
            blocks [bi1, ..., bini] corresponds to a possible meaning of the
            input string.

        Note:
            In this implemenation, only one meaning is available.
        """
        if DEBUG:
            UI.render_info('compute_blocks(...) called for word ' + self.string)

        if not compute_ethym:
            blocks = [Block(self.string_without_suffix[i]) \
                            for i in range(len(self.string_without_suffix)) \
                            if self.string_without_suffix[i] != ' ']
        else:
            ethym = get_hanja(self.string_without_suffix)
            if DEBUG:
                UI.render_info(ethym)

            blocks = [Block(self.string_without_suffix[i], ethym=ethym[i], \
                        meaning=get_hanja_meaning(ethym[i]), \
                        name=get_hanja_name(ethym[i])) \
                        for i in range(len(self.string_without_suffix)) \
                        if self.string_without_suffix[i] != ' ']

        if self.suffix:
            suffix_desc = 'Suffix: ' + self.suffix_meaning
            blocks.append(Block(self.suffix, meaning=suffix_desc))

        return [blocks]


#==============================================================================
# LANGUAGE METHODS
#==============================================================================

def get_words_with_block(block, exclude=None):
    """
    This functions returns a list of Korean words which also contains blocks
    with the same ethymology.

    When the ethymology is not available, an empty list is returned. This
    typically happens when the input block is a suffix.
    """
    if block.get_ethym():
        query = """SELECT * FROM `Korean` WHERE INSTR( ethym, '""" + \
                                            block.get_ethym() + """') >0"""
        engine = create_engine(login.connection_string, echo=False)
        results = pd.io.sql.execute(query, engine)
        results = results.fetchall()
        words = [KoreanWord(string=r[0], ethym=r[1], meaning=r[2]) \
                    for r in results if r[0] != exclude and \
                    len(r[0]) == len(r[1]) and \
                    tools.detect_language(r[1]) is not 'korean']
                    # len check and ethym check to avoid some corrupted
                    # data from the database to be displayed
    else:
        words = []

    return words

def get_hanja_meaning(hanja):
    """ Get the meaning of a hanja character from the database """
    if DEBUG:
        UI.render_info('get_hanja_meaning(...) called with hanja=' + hanja)
    query = "SELECT meaning from Korean_ethym WHERE ethym='" + hanja + "'"
    engine = create_engine(login.connection_string, echo=False)
    results = pd.io.sql.execute(query, engine)
    results = results.fetchall()
    if results:
        return results[0][0]
    else:
        return None

def get_hanja_name(hanja):
    """ Get the name of a hanja character from the database """
    query = "SELECT name from Korean_ethym WHERE ethym='" + hanja + "'"
    engine = create_engine(login.connection_string, echo=False)
    results = pd.io.sql.execute(query, engine)
    results = results.fetchall()
    if results:
        return results[0][0]
    else:
        return None


