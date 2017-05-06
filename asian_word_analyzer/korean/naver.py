#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request

from bs4 import BeautifulSoup


def get_hanja(hangul):
    """ 
    Get the hanja representation of a Korean word by querying and parsing Naver.
    """
    search = ''.join('%' + "{:02x}".format(a) for a in hangul.encode('utf8'))

    # url = u"http://hanja.naver.com/search?query=휴업" # not supported by urllib
    # url = 'http://hanja.naver.com/search?query=' + search
    url = 'http://endic.naver.com/search.nhn?sLn=kr&query=' + search

    contents = urllib.request.urlopen(url).read()
    contents.decode('utf8')

    soup = BeautifulSoup(contents)
    first = soup.find('dt', {'class':'first'})
    strings = [s for s in first.stripped_strings]
    hanja = strings[-1]

    if hanja is not '.':
        return hanja
    else:
        return None
