# -*- coding: utf-8 -*-

import pandas as pd
from sqlalchemy import create_engine

from asian_word_analyzer.korean.word import KoreanWord
import asian_word_analyzer.login as login
from asian_word_analyzer.UI import render_info
from asian_word_analyzer.tools import detect_language

DEBUG = False


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
                    detect_language(r[1]) is not 'korean']
                    # len check and ethym check to avoid some corrupted
                    # data from the database to be displayed
    else:
        words = []

    return words

def get_hanja_meaning(hanja):
    """ Get the meaning of a hanja character from the database """
    if DEBUG:
        render_info('get_hanja_meaning(...) called with hanja=' + hanja)
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

def compute_meanings(word):
    """ Find the possible meanings based on the input string by the user"""
    query = "SELECT meaning from Korean WHERE word='{}'".format(word)
    engine = create_engine(login.connection_string, echo=False)
    results = pd.io.sql.execute(query, engine)
    results = results.fetchall()
    if results:
        return results[0]
    else:
        return ['']
