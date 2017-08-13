import re
import datetime
import pandas as pd
import sqlite3 as lite
from portfolio_processor import fix_known_mistakes,filter_index,configure_excel,get_missing_symbols,\
get_year_start_values
con = lite.connect("portfolio_data.db")
cur = con.cursor()

raw = pd.read_excel(r'C:\Users\Yasch\Downloads\Joint 2A Trust Copy (4).xlsx').iloc[:,:4]
raw.columns = ['symbols', 'Qty', 'Open_date', 'cps']
raw.set_index('symbols', inplace=True)
raw.dropna(inplace=True)
raw_index = raw.index

def test_fix_known_mistakes():
    """Test that the NEW and the '+' insn't  in the string
    also test each string has parentheses with text"""
    for i in fix_known_mistakes(raw_index):
        assert re.search(r'''\+''', i)    == None
        assert re.search(r'''TSO''',i)    == None
        assert re.search(r'''NEW''', i) == None
        assert re.search(r'''\(.+\)''',i) != None

def test_filter_index():
    assert filter_index(['The AAPL COMPANY (AAPL)', 'Alphabet (GOOG)']) == ['AAPL' , 'GOOG']

def test_configure_excel():
    raw = pd.read_excel(r'C:\Users\Yasch\Downloads\Joint 2A Trust Copy (4).xlsx').iloc[:,:4]
    assert len(configure_excel(raw)) == 128

def test_get_missing_symbols():
    symbols_to_test = ['AAPL', 'GOOGL', 'MSFT', 'JNJ', 'TSLA', 'JPM', 'PEP', 'KO']
    get_missing_symbols(symbols_to_test)
    for i in symbols_to_test:
        assert (cur.execute("SELECT Date FROM %s LIMIT 1"%i))

def test_get_year_start_values():
    configed = configure_excel(raw)
    get_year_start_values(configed)
    print (configed.columns)
    for i in ['year_start_2007', 'year_start_2008',
       'year_start_2009', 'year_start_2010', 'year_start_2011',
       'year_start_2012', 'year_start_2013', 'year_start_2014',
       'year_start_2015', 'year_start_2016', 'year_start_2017']:
        assert i in configed.columns

test_get_year_start_values()