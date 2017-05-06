#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:17:12 2015

@author     Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
@version    June 2015
"""


def detect_language(word, raise_if_unknown=False):
    """ Basic language detection based on the unicode of the first character.

    Input:
        Unicode string (type 'unicode' in Python2, 'str' in Python3)

    Output:
        'korean', 'thai'

    """

    if ((ord(word[0]) >= int('0xAC00', 0) and ord(word[0]) <= int('0xD7AF', 0)) or 
        (ord(word[0]) >= int('0x1100', 0) and ord(word[0]) <= int('0x11FF', 0)) or 
        (ord(word[0]) >= int('0x3130', 0) and ord(word[0]) <= int('0x318F', 0)) or 
        (ord(word[0]) >= int('0x3200', 0) and ord(word[0]) <= int('0x32FF', 0)) or 
        (ord(word[0]) >= int('0xA960', 0) and ord(word[0]) <= int('0xA97F', 0)) or 
        (ord(word[0]) >= int('0xD7B0', 0) and ord(word[0]) <= int('0xD7FF', 0)) or 
        (ord(word[0]) >= int('0xFF00', 0) and ord(word[0]) <= int('0xFFEF', 0))):
            return 'korean'
    elif (ord(word[0]) >= int('0x1100', 0) and ord(word[0]) <= int('0x11FF', 0)) or \
         (ord(word[0]) >= int('0x0E01', 0) and ord(word[0]) <= int('0x0E5B', 0)):
        return 'thai'
    else:
        if raise_if_unknown:
            raise ValueError('Unknown or unsupported language')
        else:
            return 'unknown'


