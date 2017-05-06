# -*- coding: utf-8 -*-

from asian_word_analyzer.utf8 import _u

# consonants
C = '[ก-ฮ]'
# low class consonants
LC = '[งนมรนยญวล]'
# consonant clusters
CC = '(กร|กล|กว|ขร|ขล|ขว|คร|คล|คว|ปร|ปล|ผล|พร|พล|ตร)'
# all consonants
AC = '({c} | {cc})'.format(c=C, cc=CC)
# AC = _u('({c} )'.format(c=C))
# leading vowels
F = '[เ-ไ]'  # 'เ,แ,ไ,ใ,โ'
# trailing vowels
R = '[ะาำๅ]'  # ะ,า,◌ำ,
R1 = '[าำๅ]'  # า,◌ำ,ๅ
# upper vowels
U = '[ัิีึื]'  # ◌ั, ◌ิ, ◌ี, ◌ึ, ◌ื,◌
U1 = '[ิีึื]'  # ◌ิ, ◌ี, ◌ึ, ◌ื,◌
# lower vowels
L = '[ุู]'  # ◌ุ,◌ู,◌
# tonal marks
T = '[่-๋]'
# final consonants (not followed by tonal mark or vowel)
Z = '[กขฃคฅฆงจชซญฎฏฐฑฒณดตถทธนบปพฟภมรฤลฦศษสฬวย](?!{t}|{u}|{l}|{r})'.format(t=T, u=U, l=L,r=R)
# silent syllables
S = '{c}({u}|{l})?{t}?์{{1}}'.format(c=C, u=U, l=L, t=T)
# consonants incl. initial silent consonants 
c1 = '({cc}|ห{lc}|อย|{c})'.format(lc=LC, c=C, cc=CC)
# initial consonant + vowel (upper/lower/trailing/inherent) + final consonant
r3 = _u('({c1}{c}?({c}{{0}}|({l}|{u})?{t}?|{t}?{r}|{t}?อ){z}({s})?)'.format(c=C, c1=c1, u=U, l=L,
                                                                            r=R1, t=T, z=Z, s=S))
# initial consonant + vowel (upper/lower/trailing) 
r4 = _u('({c}({t}?อ|({l}|{u}){t}?|{t}?{r})์?)'.format(c=c1, u=U1, l=L, r=R, t=T))
# leading vowel
r5 = _u('({f}{c}(็?{t}?{z}|{t}?{r}?|{u}?{t}?{z}))'.format(f=F, c=c1, t=T, r=R, u=U, z=Z))
# sara ia and sara uea
r6 = _u('เ{c}(ี{t}?ย|ื{t}?อ)({z}|ว)?'.format(c=c1, t=T, z=Z))
# er, o, ao
r7 = _u('({}{}(อ|า)ะ?)'.format(F, c1))
# double r
r8 = _u('({c}รร{z}?)'.format(c=c1, z=Z))
