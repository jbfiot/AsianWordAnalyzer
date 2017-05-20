#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Wed Apr 22 11:31:22 2015

@author:    Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
"""


import cgitb

from asian_word_analyzer.utf8 import _u
from asian_word_analyzer.korean.naver import get_hanja
from asian_word_analyzer.korean.db import DbUtil
from asian_word_analyzer.block import Block
import asian_word_analyzer.ui as ui
from asian_word_analyzer.words import AsianWord


cgitb.enable()


class KoreanWord(AsianWord):
    """ This class is used to manipulate Korean words. """
    language = 'Korean'

    def __init__(self, string='', etymology=None, meaning=None, compute_etymology=False):
        self.check_init_parameters(string, etymology, meaning)
        self.string = _u(string)  # e.g. user input string
        self.db_util = DbUtil()

        if etymology and meaning:
            self.blocks = [[Block(string[i], etymology=etymology[i]) for i in range(len(string))]]
            self.meanings = [meaning]
            self.selected_meaning = 0  # the word is clearly defined

        else:
            self.compute_suffix()
            self.blocks = self.compute_blocks(compute_etymology)
            self.meanings = self.db_util.compute_meanings(self.string_without_suffix) # Different meanings in English
            self.selected_meaning = 0  # index of the selected meaning

    @staticmethod
    def check_init_parameters(string, etymology, meaning):
        if etymology is not None:
            if len(string) != len(etymology):
                # to the best of my knowledge a Korean word and its hanja
                # representation (when existing) have the same lengths
                raise ValueError('string and etymology must have the same lengths')

    def compute_suffix(self):
        """ This method computes:
        self.suffix
        self.suffix_meaning
        self.string_without_suffix
        """
        suffixes = {u'하다': u'하다 verb particle',
                    u'합니다': u'formal 하다 ending',
                    u'하세요': u'formal imperative form of 하다',
                    u'요': u'politeness particle',
                    u'님': u'honorific particle'}
        # TODO: store the suffixes in the database instead of hardcoding them here

        detected_suffix = ''
        for suffix in suffixes.keys():
            if self.string.endswith(suffix):
                detected_suffix = suffix
                continue
        self.string_without_suffix = self.string[0:len(self.string)-len(detected_suffix)]
        self.suffix = detected_suffix
        self.suffix_meaning = suffixes.get(detected_suffix, None)

    def compute_blocks(self, compute_etymology=False):
        """ Compute the blocks given the input string.

        Output:
            Returns a list of lists of blocks, i.e.
            [ [b11, ..., b1n1], [b21, ..., b2n2], ...], where each list of
            blocks [bi1, ..., bini] corresponds to a possible meaning of the
            input string.

        Note:
            In this implementation, only one meaning is available.
        """
        ui.render_debug('compute_blocks(...) called for word ' + self.string)

        if compute_etymology:
            etymology = get_hanja(self.string_without_suffix)
            ui.render_debug(etymology)

            blocks = [Block(self.string_without_suffix[i], etymology=etymology[i],
                            meaning=self.db_util.get_hanja_meaning(etymology[i]),
                            name=self.db_util.get_hanja_name(etymology[i]))
                      for i in range(len(self.string_without_suffix))
                      if self.string_without_suffix[i] != ' ']
        else:
            blocks = [Block(self.string_without_suffix[i])
                      for i in range(len(self.string_without_suffix))
                      if self.string_without_suffix[i] != ' ']

        if self.suffix:
            suffix_desc = 'Suffix: ' + self.suffix_meaning
            blocks.append(Block(self.suffix, meaning=suffix_desc))

        return [blocks]

