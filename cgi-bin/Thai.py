#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
"""
Created on Wed Apr 22 11:31:22 2015

@author: jbfiot
"""

import re   # for parsing regular expressions

FILE = '/home/jbfiot/www/cgi-bin/data/thai.txt'


# consonants
C = u'[ก-ฮ]'
# low class consonants
LC = u'[งนมรนยญวล]'
# consonant clusters
CC = u'(กร|กล|กว|ขร|ขล|ขว|คร|คล|คว|ปร|ปล|ผล|พร|พล|ตร)'
# all consonants
AC = u'({} | {})'.format(C, CC)
# leading vowels
F = u'[เ-ไ]' # 'เ,แ,ไ,ใ,โ'
# trailing vowels
R = u'[ะาำๅ]'  # ะ,า,◌ำ,
R1 = u'[าำๅ]'  # า,◌ำ,ๅ
# upper vowels
U = u'[ัิีึื]' # ◌ั, ◌ิ, ◌ี, ◌ึ, ◌ื,◌
U1 = u'[ิีึื]' # ◌ิ, ◌ี, ◌ึ, ◌ื,◌
# lower vowels
L = u'[ุู]' # ◌ุ,◌ู,◌
# tonal marks
T = u'[่-๋]'
# final consonants (not followed by tonal mark or vowel)
Z = u'[กขฃคฅฆงจชซญฎฏฐฑฒณดตถทธนบปพฟภมรฤลฦศษสฬวย](?!{t}|{u}|{l}|{r})'.format(t=T, u=U, l=L,r=R)
# silent syllables
S = u'{c}({u}|{l})?{t}?์{{1}}'.format(c=C,u=U,l=L,t=T)

suffixes = {}

def get_meaning(word):
    f = open(FILE, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        if line.split(',')[0].strip() == word:
            return line.split(',')[1].strip()
    return ''

def get_words_with_block(block, exclude=None):
    f = open(FILE, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    words = {}
    for line in lines:
        if block in get_blocks(line.split(',')[0]):
            word = line.split(',')[0].strip()
            if word != exclude:
                words[word] = line.split(',')[1].strip()
    return words
    

def get_blocks(txt):
    blocks = {}

    #first vowel, single consonant
    r1 = u'([เ-ไ][ก-อ][่-๋]?)'  
    #first vowel, initial + final cons.
    r2 = u'([เ-โ][ก-อ][่-๋]?[ก-อ])'
    # consonants incl. initial silent consonants 
    c1 = u'({cc}|ห{lc}|อย|{c})'.format(lc=LC, c=C, cc=CC)
    # initial consonant + vowel (upper/lower/trailing/inherent) + final consonant
    r3 = u'({c1}{c}?({c}{{0}}|({l}|{u})?{t}?|{t}?{r1}|{t}?อ){z}({s})?)'.format(c=C, c1=c1,u=U,l=L,r1=R1,r=R,t=T,z=Z,s=S)
    # initial consonant + vowel (upper/lower/trailing) 
    r4 = u'({c}({t}?อ|({l}|{u}){t}?|{t}?{r})์?)'.format(c=c1, u=U1, l=L, r=R, t=T)
    # leading vowel
    r5 = u'({f}{c}(็?{t}?{z}|{t}?{r}?|{u}?{t}?{z}))'.format(f=F,c=c1,t=T,r=R,u=U,z=Z,l=L)
    # sara ia and sara uea
    r6 = u'เ{c}(ี{t}?ย|ื{t}?อ)({z}|ว)?'.format(c=c1,t=T,z=Z)
    # er, o, ao
    r7 = u'({f}{c}(อ|า)ะ?)'.format(f=F,c=c1,t=T,r=R,u=U,z=Z)
    ## double r
    r8 = u'({c}รร{z}?)'.format(f=F,c=c1,t=T,r=R,u=U,z=Z)

    regexp = u'('+ r8 + '|' + r7 + '|' + r3 + '|' + r6 + '|' + r4 + '|' + r5 + ')'
    
    regex = re.compile(regexp)
    patterns = regex.finditer(txt)

    for i in patterns:
        block = i.group()#.decode('utf-8')
        if block in blocks:
            blocks[block] += 1
        else:
            blocks[block] = 1


    return blocks
