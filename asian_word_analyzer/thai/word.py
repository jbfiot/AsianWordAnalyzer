#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Wed Apr 22 11:31:22 2015

@author:    Jonas C. Villumsen
@version:   June 2015
"""


import cgitb
import re
from collections import defaultdict

from asian_word_analyzer.block import Block
import asian_word_analyzer.ui as ui
from asian_word_analyzer.utf8 import _u
from asian_word_analyzer.thai.db import DbUtil
from asian_word_analyzer.thai.symbol_classes import r3, r4, r5, r6, r7, r8
from asian_word_analyzer.words import AsianWord

cgitb.enable()


class ThaiWord(AsianWord):
    """ This class is used to manipulate Thai words. """
    def __init__(self, string='', meaning=None, compute_ethym=False):
        self.string = string  # e.g. user input string
        self.language = 'Thai'
        self.blocks = [self.compute_blocks(self.string)]
        self.selected_meaning = 0  # index of the selected meaning
        self.meanings = DbUtil().compute_meanings(string)  # Different meanings in English
        ui.render_info(self.meanings.head())

    @staticmethod
    def compute_blocks(txt, method='syllable'):
        """
        Compute blocks for word based on regular expressions
        
        Generates a dictionary of (block, number) pairs, where block is the string representation of 
        the block and number is the number of times this block occurs in txt.
        
        Returns only the blocks.
        """
        
        blocks = defaultdict(int)
    
        if method == 'word':
            regexp = _u('บัตร|ประ|จำ|ตัว')
        elif method == 'syllable':
            regexp = _u('(' + r8 + '|' + r7 + '|' + r3 + '|' + r6 + '|' + r4 + '|' + r5 + ')')
        else:
            raise ValueError('Unsupported method: {}'.format(method))
    
        regex = re.compile(regexp)
        patterns = regex.finditer(_u(txt))
    
        for i in patterns:
    
            block = Block(_u(i.group()))
            blocks[block] += 1

        # compute block meanings
        blocks = DbUtil().compute_block_meanings(blocks)
    
        return blocks.keys()
