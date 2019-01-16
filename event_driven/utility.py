# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3

# from jqdatasdk import *
# auth('15221679228','password')

conn = sqlite3.connect('data.db')


def get_industry_data():
    ind_data = pd.read_sql('Select * from industry', conn, index_col='date',
                           parse_dates=['date'])
    return ind_data


def get_index_data():
    index_data = pd.read_sql("select * from 'index'", conn,
                             index_col='date', parse_dates=['date'])
    return index_data

def get_stock_data(stock_list):
    sql_command = "select * from stock where stkcode IN {stock_list}"
    stock_data = pd.read_sql(sql_command.format(stock_list=stock_list),
                             conn, parse_dates=['date'])
    return stock_data

def get_stock_industry():
    stock_ind_data = pd.read_sql("select * from stock_industry", conn)
    return stock_ind_data


# def get_index_data(index_list=None):
#     index_list = ['000001.XSHG', '399001.XSHE', '399005.XSHE', '399006.XSHE',
#                   '000016.XSHG','000016.XSHG', '000300.XSHG',
#                   '000905.XSHG'] if index_list is None else index_list
#     index_hist = {}
#     for index in index_list:
#         hist = get_price(index, start_date='2008-12-31', end_date='2018-12-31')
#         hist['ret'] = hist['close'].pct_change()
#         hist.dropna(inplace=True)
#         index_hist[index] = hist
#     return(index_hist)

def get_plot_title(time_interval, event_name, index=True):
    if index:
        obj = '主要指数'
    else:
        obj = '一级行业板块'
    return (obj + event_name + '日平均日收益率' + str(time_interval))
