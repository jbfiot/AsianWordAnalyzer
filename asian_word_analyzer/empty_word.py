#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Mon Jun  1 15:53:28 2015

@author:    Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
"""



import cgitb
cgitb.enable()


class EmptyWord(object):
    def __init__(self):
        self.string = ''
        self.language = ''
        self.meaning = ''
        self.ethym = ''

