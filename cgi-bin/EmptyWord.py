#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Mon Jun  1 15:53:28 2015

@author:    Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
@version:   June 2015
"""


#==============================================================================
# MODULES
#==============================================================================

# CGI debugging
import cgitb
cgitb.enable()



class EmptyWord(object):
    """ This class is used to manipulate Korean words. """
    def __init__(self):
        self.string = ''
        self.language = ''
        self.meaning = ''

#==============================================================================
#  GETTERS
#==============================================================================

    def get_string(self):
        """ String getter """
        return self.string

    def get_language(self):
        """ Language getter """
        return self.language

    def get_blocks(self):
        """ Blocks getter """
        return self.blocks

    def get_meaning(self):
        """ Meaning getter """
        return self.meaning

    def get_blocks_for_selected_meaning(self):
        """ Getter for the blocks corresponding to the selected meaning """
        return self.blocks[self.selected_meaning]


#==============================================================================
#  PRINT METHODS
#==============================================================================

    def print_blocks_for_selected_meaning(self):
        """ This methods prints the block strings for the selected meaning.

        Example:
        --------
            For the word '안녕', the blocks will be ['안', '녕']
        """
        return [block.get_str() for block in self.blocks[self.selected_meaning]]


