# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 11:35:01 2016

@author:     Jean-Baptiste Fiot  <jean-baptiste.fiot@centraliens.net>
"""

import sys

# Handy functions when dealing with UTF8 strings
if sys.version_info.major == 2:
    # guarantee unicode string
    _u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t, str) else t
    _uu = lambda *tt: tuple(_u(t) for t in tt)
    # guarantee byte string in UTF8 encoding
    _u8 = lambda t: t.encode('UTF-8', 'replace') if isinstance(t, unicode) else t
    _uu8 = lambda *tt: tuple(_u8(t) for t in tt)
else:
    # guarantee unicode string
    _u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t, bytes) else t
    _uu = lambda *tt: tuple(_u(t) for t in tt)
    # guarantee byte string in UTF8 encoding
    _u8 = lambda t: t.encode('UTF-8', 'replace') if isinstance(t, str) else t
    _uu8 = lambda *tt: tuple(_u8(t) for t in tt)