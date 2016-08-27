#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 13:33:39 2015

Note:
This code is not fully compatible to Python3, because of the SQLalchemy used
for database interaction via pandas.

@author:    Jean-Baptiste Fiot < jean-baptiste.fiot@centraliens.net >
@version:   July 2015
"""

import pandas as pd
from sqlalchemy import create_engine
import login
engine = create_engine(login.connection_string, echo=False)


def fill_Korean_Ethym():
    """ This function fills the "Korean_ethym" table in the database with the
    hanjas from the CSV"""
    # TODO: add dtype to specify columns types
    df = pd.read_csv('../data/hanja_list.csv')
    df.to_sql('Korean_ethym', engine, if_exists='replace', index=False)


if __name__ == '__main__':
    fill_Korean_Ethym()