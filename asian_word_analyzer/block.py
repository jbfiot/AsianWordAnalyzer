# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 11:35:59 2015

@author:    Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
@version:   June 2015
"""

class Block(object):
    """ This class is used to manipulate the word blocks.

    Example:
    --------
    As an example, 안녕 is a Korean word with two syllables.
    In general, 안녕 means peace, stability, and originates from 安寧.
    We can represent the word 안녕 as a list of two blocks:
    Block 1:
        block_str: 안
        ethymology: 安
        name: 편안할 안, 어찌 안
        meaning: ?
    Block 2:
        block_str: 녕
        ethymology: 寧
        name: 편안할 녕
        meaning: ?
    """

    def __init__(self, string, ethym=None, name=None, meaning=None):
        """ Constructor """
        self.string = string
        self.ethym = ethym
        self.name = name
        self.meaning = meaning
