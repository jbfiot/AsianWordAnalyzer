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
        self.cursor.execute(query)
        meanings = self.cursor.fetchall()
        return [meaning[0] for meaning in meanings] if meanings else ['']

    def get_hanja_x(self, hanja, x):
        query = "SELECT {} from Korean_etymology WHERE etymology='{}'".format(x, hanja)
        self.cursor.execute(query)
        hanja_x = self.cursor.fetchone()
        return hanja_x[0] if hanja_x else None

    get_hanja_meaning = partialmethod(get_hanja_x, x='meaning')

    get_hanja_name = partialmethod(get_hanja_x, x='name')

    def get_words_with_block(self, block, exclude=None) -> [tuple]:
        """
        This functions returns a list of Korean words which also contains blocks
        with the same etymology.
    
        When the etymology is not available, an empty list is returned. This
        typically happens when the input block is a suffix.
        """
        if block.etymology:
            query = """SELECT word, etymology, meaning FROM `Korean` 
                       WHERE etymology LIKE '%{}%'
                       AND length(word) = length(etymology)
                       """.format(block.etymology)
            if exclude:
                query += """ AND word != '{}'""".format(exclude)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            words = [r for r in results if detect_language(r[1]) is not 'korean']

        else:
            words = []
    
        return words
