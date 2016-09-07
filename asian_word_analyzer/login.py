#!/usr/bin/python
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Wed Apr 22 11:31:22 2015

@author     Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
"""

import os


folder = os.path.split(os.path.realpath(__file__))[0]
connection_string = os.path.join(folder, 'data/korean.sqlite')
