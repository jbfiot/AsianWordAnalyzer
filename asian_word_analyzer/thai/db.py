# -*- coding: utf-8 -*-


import codecs
import os
import pandas as pd

from asian_word_analyzer.utf8 import _u

folder = os.path.split(os.path.realpath(__file__))[0]
FILE = os.path.join(folder, '../data/thai.txt')


class DbUtil:
    def __init__(self):
        f = codecs.open(FILE, 'r', encoding='utf-8')
        self.lines = f.readlines()
        f.close()
        self.data = pd.read_csv(FILE)

    def get_words_with_block(self, block, exclude=None):
        """
        This functions returns a list of Thai words that rely on the same block.
        """    
#        words = []
#        for line in self.lines:
#            if _u(block.string) in line.split(',')[0]:
#                word = line.split(',')[0].strip()
#                if word != exclude:
#                    words.append(ThaiWord(string=word, \
#                                            meaning=line.split(',')[1].strip()))
#    
#        return words
        return self.data

    def compute_block_meanings(self, blocks):
        for line in self.lines:
            for block in blocks:
                if _u(block.string) == line.split(',')[0]:
                    meaning = line.split(',')[1].strip()
                    block.meaning = meaning
        return blocks

    def compute_meanings(self, string):
        return self.data[self.data.word == string].meaning
        for line in self.lines:            
            if line.split(',')[0] == string:
                return [line.split(',')[1].strip()]
        return ['']
