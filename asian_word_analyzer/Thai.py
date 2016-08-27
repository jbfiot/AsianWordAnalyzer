#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Wed Apr 22 11:31:22 2015

@author:    Jonas C. Villumsen
@version:   June 2015
"""


#==============================================================================
# MODULES
#==============================================================================

# Encoding
#import locale                                  # Ensures that subsequent open()s 
#locale.getpreferredencoding = lambda: 'UTF-8'  # are UTF-8 encoded.
#utf8stdout = open(1, 'w', encoding='utf-8', closefd=False) # fd 1 is stdout
#from functools import partial
#utf8print = partial(print, end='\r\n', file=utf8stdout)
#utf8print = partial(print, end='\n', file=utf8stdout)
import codecs

# CGI debugging
import cgitb
cgitb.enable()
DEBUG = 0

# AWA components
from Block import Block
import UI

# Web requests
#import urllib.request
#import urllib2

# Method 
METHOD = 'dic' # available methods: 'dic', 'Naver' (to be implemented)

# Dictionnary
FILE = '../data/thai.txt'


from asian_word_analyzer.utf8 import _u

#==============================================================================
# SYMBOL CLASSES
#==============================================================================
# consonants
C = '[ก-ฮ]'
# low class consonants
LC = '[งนมรนยญวล]'
# consonant clusters
CC = '(กร|กล|กว|ขร|ขล|ขว|คร|คล|คว|ปร|ปล|ผล|พร|พล|ตร)'
# all consonants
AC = '({c} | {cc})'.format(c=C, cc=CC)
#AC = _u('({c} )'.format(c=C))
# leading vowels
F = '[เ-ไ]' # 'เ,แ,ไ,ใ,โ'
# trailing vowels
R = '[ะาำๅ]'  # ะ,า,◌ำ,
R1 = '[าำๅ]'  # า,◌ำ,ๅ
# upper vowels
U = '[ัิีึื]' # ◌ั, ◌ิ, ◌ี, ◌ึ, ◌ื,◌
U1 = '[ิีึื]' # ◌ิ, ◌ี, ◌ึ, ◌ื,◌
# lower vowels
L = '[ุู]' # ◌ุ,◌ู,◌
# tonal marks
T = '[่-๋]'
# final consonants (not followed by tonal mark or vowel)
Z = '[กขฃคฅฆงจชซญฎฏฐฑฒณดตถทธนบปพฟภมรฤลฦศษสฬวย](?!{t}|{u}|{l}|{r})'.format(t=T, u=U, l=L,r=R)
# silent syllables
S = '{c}({u}|{l})?{t}?์{{1}}'.format(c=C,u=U,l=L,t=T)



#==============================================================================
# LANGUAGE METHODS
#==============================================================================

def get_words_with_block(block, exclude=None):
    """
    This functions returns a list of Thai words that rely on the same block.
    """
    
    # DICTIONNARY IMPLEMENTATION
    if METHOD == 'dic':
        f = codecs.open(FILE, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        words = []
        for line in lines:
            # Implementation 1: using hangul syllables
            if _u(block.get_string()) in line.split(',')[0]:
                word = line.split(',')[0].strip()
                if word != exclude:
                    words.append(ThaiWord(string=word, \
                                            meaning=line.split(',')[1].strip()))

        return words

def compute_block_meanings(blocks):
    # DICTIONNARY IMPLEMENTATION
    if METHOD == 'dic':
        f = codecs.open(FILE, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        for line in lines:
            for block in blocks:
                if _u(block.get_string()) == line.split(',')[0]:
                    meaning = line.split(',')[1].strip()
                    block.meaning = meaning
        return blocks

def compute_blocks_re(txt):
    """Compute blocks for word based on regular expressions
       Generates a dictionary of (block, number) pairs,
       where block is the string representation of the block
       and number is the number of times this block occurs in
       txt.
       Returns only the blocks."""
    import re

    METHOD = 'syllable'

    blocks = {}

    if METHOD == 'word':
        regexp = _u('บัตร|ประ|จำ|ตัว')
    elif METHOD == 'syllable':
        # consonants incl. initial silent consonants 
        c1 = '({cc}|ห{lc}|อย|{c})'.format(lc=LC, c=C, cc=CC)
        # initial consonant + vowel (upper/lower/trailing/inherent) + final consonant
        r3 = _u('({c1}{c}?({c}{{0}}|({l}|{u})?{t}?|{t}?{r}|{t}?อ){z}({s})?)'.format(c=C, c1=c1,u=U,l=L,r=R1,t=T,z=Z,s=S))
        # initial consonant + vowel (upper/lower/trailing) 
        r4 = _u('({c}({t}?อ|({l}|{u}){t}?|{t}?{r})์?)'.format(c=c1, u=U1, l=L, r=R, t=T))
        # leading vowel
        r5 = _u('({f}{c}(็?{t}?{z}|{t}?{r}?|{u}?{t}?{z}))'.format(f=F,c=c1,t=T,r=R,u=U,z=Z))
        # sara ia and sara uea
        r6 = _u('เ{c}(ี{t}?ย|ื{t}?อ)({z}|ว)?'.format(c=c1,t=T,z=Z))
        # er, o, ao
        r7 = _u('({}{}(อ|า)ะ?)'.format(F,c1))
        ## double r
        r8 = _u('({c}รร{z}?)'.format(c=c1,z=Z))
        regexp = _u('('+ r8 + '|' + r7 + '|' + r3 + '|' + r6 + '|' + r4 + '|' + r5 + ')')

    regex = re.compile(regexp)
    patterns = regex.finditer(_u(txt))

    for i in patterns:

        block = Block(_u(i.group()))
        if block in blocks:
            blocks[block] += 1
        else:
            blocks[block] = 1

    # compute block meanings
    blocks = compute_block_meanings(blocks)

    return blocks.keys()

    

class ThaiWord(object):
    """ This class is used to manipulate Thai words. """
    def __init__(self, string='', meaning=None, compute_ethym=False):
        self.string = string  # e.g. user input string
        self.language = 'Thai'
        self.blocks = self.compute_blocks(compute_ethym)
        self.selected_meaning = 0 # index of the selected meaning
        self.meanings = self.compute_meanings() # Different meanings in English
        
        
    #==========================================================================
    #  GETTERS
    #==========================================================================

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
        #UI.render_info(self.meanings[self.selected_meaning])
        return self.meanings[self.selected_meaning]

    def get_blocks_for_selected_meaning(self):
        """ Getter for the blocks corresponding to the selected meaning """
        return self.blocks[self.selected_meaning]

    def get_ethym(self):
        return ''.join([block.get_ethym() for block in \
                    self.blocks[self.selected_meaning] if block.get_ethym()])

    #==========================================================================
    #  PRINT METHODS
    #==========================================================================

    def print_blocks_for_selected_meaning(self):
        """ This methods prints the block strings for the selected meaning. 
        
        Example:
        --------
            For the word '안녕', the blocks will be ['안', '녕']
        """
        UI.render_info('print blocks for selected meaning')
        UI.render_info([block.get_str() for block in self.blocks[self.selected_meaning]])
        return [block.get_str() for block in self.blocks[self.selected_meaning]]
        

    #==========================================================================
    #   LANGUAGE METHODS        
    #==========================================================================
        
    def compute_meanings(self):
        """ Find the meaning.
        Note:         
        """
        f = codecs.open(FILE, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        for line in lines:
            
            if line.split(',')[0] == self.string:
                #UI.render_info(line.split(',')[0])
                return [line.split(',')[1].strip()]
        return ['']
        

    def compute_blocks(self, compute_ethym=False):
        """ Compute the blocks given the input string.

        Output:
            Returns a list of lists of blocks, i.e. 
            [ [b11, ..., b1n1], [b21, ..., b2n2], ...], where each list of 
            blocks [bi1, ..., bini] corresponds to a possible meaning of the 
            input string.

        Note: 
            In this CSV dictionnary based implemenation, only one meaning is 
            available.            
        """
        if DEBUG:
            UI.render_info('compute_blocks() called for word ' + self.string)        
        
        suffixes = {'하다':'하다 verb particule', \
            '합니다': 'formal 하다 ending', \
            '하세요': 'formal imperative form of 하다', \
              '요': 'politeness particle'}
              
        detected_suffix = ''
        # for suffix in suffixes.keys():
        #     if self.string.endswith(suffix):
        #         detected_suffix = suffix
        #         continue
        body = self.string[0:len(self.string)-len(detected_suffix)]
        #if not compute_ethym:
            #blocks = [Block(body[i]) for i in range(len(body)) if body[i] != ' ']
        blocks = compute_blocks_re(body)
        # else:
        #     hanja = get_hanja(body)
        #     if DEBUG:
        #         UI.render_info(hanja)
        #     blocks = [Block(body[i], ethym=hanja[i]) for i in range(len(body)) if body[i] != ' ']

        # if detected_suffix:
        #     suffix_desc = 'Suffix: ' + suffixes[detected_suffix]
        #     blocks.append(Block(detected_suffix, ethym=suffix_desc))

        if DEBUG:
            for block in blocks:
                UI.render_info(block.get_string())

        return [blocks]
        


