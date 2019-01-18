# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3

conn = sqlite3.connect('data.db')


def get_industry_data():
    """
    Read all the data from the table industry

    Returns
    -------
    ind_data : DataFrame
    """
    ind_data = pd.read_sql('Select * from industry', conn, index_col='date',
                           parse_dates=['date'])
    return ind_data


def get_index_data():
    """
    Read all the data from the table index

    Returns
    -------
    index_data : DataFrame
    """
    index_data = pd.read_sql("select * from 'index'", conn,
                             index_col='date', parse_dates=['date'])
    return index_data


def get_stock_data(stock_list, list_bool=True):
    """
    Read from the table stock to get the data of a stock (or stocks)

    Parameters
    ----------
    stock_list: tuple or string
        a list of stock code (stocks codes)
    list_bool: boolean, default True
        Whether to get the data of a list of stocks or a stock

    Returns
    -------
    stock_data : DataFrame
    """
    if list_bool:
        sql_command = "select * from stock where stkcode IN {stock_list}"
    else:
        sql_command = "select * from stock where stkcode = \'{stock_list}\'"

    try:
        stock_data = pd.read_sql(sql_command.format(stock_list=stock_list),
                                 conn, parse_dates=['date'])
        return stock_data
    except pd.io.sql.DatabaseError:
        return None


def get_stock_industry():
    """
    Read all the data from the table stock_industry

    Returns
    -------
    stock_ind_data : DataFrame
    """
    stock_ind_data = pd.read_sql("select * from stock_industry", conn)
    return stock_ind_data


if __name__ == '__main__':
    pass
