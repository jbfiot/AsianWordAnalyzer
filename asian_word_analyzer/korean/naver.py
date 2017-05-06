#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from bs4 import BeautifulSoup

if sys.version_info.major == 2:
    import urllib2
else:
    import urllib.request


def get_hanja(hangul):
    """ Get the hanja representation of a Korean word by querying and parsing
    Naver.
    """
    if sys.version_info.major == 2: # Python 2
        search = ''.join('%' + format(ord(a), 'x') for a in hangul.encode('utf8'))
    elif sys.version_info.major == 3: # Python 3
        search = ''.join('%' + "{:02x}".format(a) for a in hangul.encode('utf8'))

#    url = u"http://hanja.naver.com/search?query=휴업" # not supported by urllib
    url='http://hanja.naver.com/search?query=' + search
    url='http://endic.naver.com/search.nhn?sLn=kr&query=' + search


    if sys.version_info.major == 2:
        contents = urllib2.urlopen(url)
        contents = contents.read()
    else:
        contents = urllib.request.urlopen(url).read() #Python 3
        contents.decode('utf8')

    soup = BeautifulSoup(contents)
    first = soup.find('dt', {'class':'first'})
    strings = [s for s in first.stripped_strings]
    hanja = strings[-1]

    if hanja is not '.':
        return hanja
    else:
        return None