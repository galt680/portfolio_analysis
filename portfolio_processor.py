import re
import datetime
import quandl as q
import numpy as np
import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt
from my_utils import *
con = lite.connect("portfolio_data.db")
cur = con.cursor()
q.ApiConfig.api_key = 'UxWHyskR-2WjjvSsdxu4'

def fix_known_mistakes(unfiltered_index):
    """fix JPM warrants and remove NEW from some of the lines
        switches TSO to ANDV
    """
    fixed_index = []
    for i in unfiltered_index:
        try:
            if 'NEW' in i.upper():
                i = i.replace('NEW','')
            elif 'JPM+' in i:
                i = '(JPM_WS)'
            elif 'TSO' in i.upper():
                i = '(ANDV)'
            fixed_index.append(i)
        except AttributeError:
            '''can't do str on nan so need to re-add nan to index'''
            fixed_index.append(np.float64('nan'))
    return fixed_index

def filter_index(unfiltered_index):
    """takes index of title and symbol and extracts just the symbol"""
    filtered_index = []
    for i in unfiltered_index:
        try:
            #regex matches letters(case insensitive) or underscore charachter that are within paren
            filtered_index.append(re.findall(r'''\(([A-Z_?a-z]+)\)''',i)[0])
        except Exception as e:
            # print(i)
            # print(e)
            "adds ? if no symbol in there"
            filtered_index.append('?')
    return filtered_index


def configure_excel(raw_excel):
    """takes excel file and configures it to be processed by pandas"""
    raw_excel = pd.read_excel(r'C:\Users\Yasch\Downloads\Joint 2A Trust Copy (4).xlsx').iloc[:, :4]
    raw_excel.index = filter_index(fix_known_mistakes(raw_excel.index.dropna(how = 'all')))
    #renames columns of df
    raw_excel.columns =['symbols', 'Qty', 'Open_date', 'cps']
    raw_excel = raw_excel.set_index('symbols').dropna(how = 'all')

    raw_excel.index = (filter_index(fix_known_mistakes(raw_excel.index)))

    return raw_excel.drop('?')

def get_missing_symbols(symbols):
    """update each symmbol to the sql database"""
    for symbol in symbols:
        try:
            q.get("EOD/%s"%symbol).to_sql('%s'%symbol,con,if_exists='replace')
        except Exception as e:
            print(symbol,e)
            break

def get_year_start_values(configed, options = True):
    master_list_of_year_start_values = []
    for index_date in start_dates:
        year_start_value = []
        for symbol,quantity,open_date,cps in configed.reset_index().values:
            try:
            # if the stock was purchased before the year we are examining
                if open_date.year < index_date.year:
                    year_start_value.append(cur.execute(
                        "SELECT Close FROM %s WHERE DATE ='%s'"%(symbol,index_date)).fetchone()[0])
                elif  open_date.year == index_date.year:
                    if options:
                        year_start_value.append(cps)
                    else:
                        year_start_value.append(cur.execute(
                            "SELECT Close FROM %s WHERE DATE = '%s'"%(symbol,open_date)).fetchone()[0])
                else:
                    year_start_value.append(np.float64('nan'))
            except Exception as e:
                print(e)
                year_start_value.append(np.float64('nan'))
        master_list_of_year_start_values.append(year_start_value)
    for index,date in enumerate(end_dates):
        configed['year_start_%s'%date.year]= master_list_of_year_start_values[index]
    # return configed


# def get_year_end_values(configed):


start_and_end_dates = [
    [pd.Timestamp('2007-01-02'),pd.Timestamp('2007-12-31')],
    [pd.Timestamp('2008-01-02'),pd.Timestamp('2008-12-31')],
    [pd.Timestamp('2009-01-02'),pd.Timestamp('2009-12-31')],
    [pd.Timestamp('2010-01-04'),pd.Timestamp('2010-12-31')],
    [pd.Timestamp('2011-01-03'),pd.Timestamp('2011-12-30')],
    [pd.Timestamp('2012-01-03'),pd.Timestamp('2012-12-31')],
    [pd.Timestamp('2013-01-02'),pd.Timestamp('2013-12-31')],
    [pd.Timestamp('2014-01-02'),pd.Timestamp('2014-12-31')],
    [pd.Timestamp('2015-01-02'),pd.Timestamp('2015-12-31')],
    [pd.Timestamp('2016-01-04'),pd.Timestamp('2016-12-30')],
    [pd.Timestamp('2017-01-03'),pd.Timestamp('2017-06-30')]
                      ]
start_dates = [i[0] for i in start_and_end_dates]
end_dates   = [i[1] for i in start_and_end_dates]


if __name__ == "__main__":
    raw_excel = pd.read_excel(r'C:\Users\Yasch\Downloads\Joint 2A Trust Copy (4).xlsx')
    # gets first 4 columns of dataframe
    configed = (configure_excel(raw_excel))
    # get_missing_symbols(set(configed.index))
    get_year_start_values(configed)

    # get_div_values(configed)
    print (configed.columns)
