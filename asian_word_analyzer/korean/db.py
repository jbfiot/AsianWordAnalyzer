#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sqlite3
from functools import partialmethod

import pandas as pd

from asian_word_analyzer.login import connection_string
from asian_word_analyzer.tools import detect_language


class DbUtil:
    def __init__(self):
        if not os.path.isfile(connection_string):
            raise FileNotFoundError('Missing Korean database: {}'.format(connection_string))
        self.connection = sqlite3.connect(connection_string)
        self.cursor = self.connection.cursor()
        
    def compute_meanings(self, word):
        """ Find the possible meanings based on the input string by the user"""
        query = "SELECT meaning from Korean WHERE word='{}'".format(word)
        df = pd.read_sql(query, self.connection)
        if not df.empty:
            return df.meaning
        else:
            return ['']

    def get_hanja_x(self, hanja, x):
        query = "SELECT {} from Korean_etymology WHERE etymology='{}'".format(x, hanja)
        df = pd.read_sql(query, self.connection)
        if not df.empty:
            return df[x][0]
        else:
            return None

    get_hanja_meaning = partialmethod(get_hanja_x, x='meaning')

    get_hanja_name = partialmethod(get_hanja_x, x='name')

    def get_words_with_block(self, block, exclude=None):
        """
        This functions returns a list of Korean words which also contains blocks
        with the same etymology.
    
        When the etymology is not available, an empty list is returned. This
        typically happens when the input block is a suffix.
        """
        if block.etymology:
            query = """SELECT * FROM `Korean` WHERE etymology LIKE '%{}%'""".format(block.etymology)
            df = pd.read_sql(query, self.connection)
            # TODO: add the exclude filter (+ filters for corrupted rows)
            return df

#            results = pd.io.sql.execute(query, self.connection)
#            results = results.fetchall()
#            words = [KoreanWord(string=r[0], etymology=r[1], meaning=r[2]) \
#                        for r in results if r[0] != exclude and \
#                        len(r[0]) == len(r[1]) and \
#                        detect_language(r[1]) is not 'korean']
#                        # len check and etymology check to avoid some corrupted
#                        # data from the database to be displayed
        else:
            words = []
    
        return words





