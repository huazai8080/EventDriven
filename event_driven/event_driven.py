# -*- coding: utf-8 -*-
import pandas as pd
import utility
from errors import *
from baidu_spider import BaiduIndex
from datetime import datetime as dt


class EventDriven(object):
    def __init__(self):
        self.__data = {'industry': utility.get_industry_data(),
                       'index': utility.get_index_data(),
                       'stock_ind': utility.get_stock_industry()
                       }
        self.__trading_date = self.__data['industry'].index.unique()
        self.__all_date = pd.date_range(self.__trading_date[0],
                                        self.__trading_date[-1])
        self.__event_date = None
        self.__event = None
        self.__event_influenced_date = None
        self.rrr_date = [pd.to_datetime(time) for time in
                         ['2018-10-15 ', '2018-07-05', '2018-04-25',
                          '2016-03-01', '2015-10-24', '2015-09-06',
                          '2015-06-28', '2015-04-20',
                          '2015-02-05', '2012-05-18', '2012-02-24',
                          '2011-12-05']]

    @staticmethod
    def __raise_error(exception_type, details):
        """
        Get the periods during which an event has profound effects

        Parameters
        ----------
        exception_type: BaseError
            the class of the error
        details: string
            the description of the error
        """
        raise exception_type(details)

    def __get_event_influenced_date(self):
        """
        Get the periods during which an event has profound effects

        Returns
        -------
        event_influenced_date : list
        """
        event_influenced_date = {}
        baidu_index = self.get_baidu_index(keywords=self.__event)
        for date in self.__event_date:
            subset_range = pd.date_range(start=date - pd.Timedelta('30 days'),
                                         periods=60, freq='D')
            data = baidu_index.reindex(subset_range)
            data = data[data['index'] >= 3 * data['index'].median()]
            if data.empty:
                event_influenced_date[date] = pd.date_range(start=date,
                                                            periods=1,
                                                            freq='D')
            else:
                event_influenced_date[date] = pd.date_range(
                    start=data.index[0],
                    end=data.index[-1])
        return event_influenced_date

    @staticmethod
    def get_baidu_index(keywords, start_date='2011-01-01',
                        end_date=dt.now().strftime('%Y-%m-%d')):
        """
        Get the Baidu Index for a keyword from a specified time interval

        Parameters
        ----------
        keywords: string
            the keyword to search
        start_date: string, default '2011-01-01'
            the beginning of the time interval
        end_date: string, default today
            the end of the time interval

        Examples
        --------
        >> get_baidu_index('降准', '2019-01-11', '2019-01-15')
                    index
        date
        2019-01-11	2117
        2019-01-12	1252
        2019-01-13	1304
        2019-01-14	1912
        2019-01-15	3604

        Returns
        -------
        baidu_df : DataFrame
        """
        baidu_index = BaiduIndex(keywords, start_date, end_date)
        baidu_df = pd.DataFrame(baidu_index(keywords, 'all'))
        baidu_df.set_index('date', inplace=True)
        baidu_df = baidu_df[baidu_df['index'] != '']
        baidu_df['index'] = baidu_df['index'].astype(int)
        baidu_df.index = pd.to_datetime(baidu_df.index)
        return baidu_df

    def fit(self, event_date, event_name, display=True):
        """
        Get the periods during which an event has profound effects

        Parameters
        ----------
        event_date: list
            a list of all event dates
        event_name: string
            the name of the event
        display: boolean, default True
            Whether to display the result or not

        Examples
        --------
        >> fit([pd.to_datetime('2018-10-15')], '降准')
        {Timestamp('2018-10-15 00:00:00'):
            DatetimeIndex(['2018-10-07',
                '2018-10-08',
                '2018-10-09',
                '2018-10-10',
                '2018-10-11',
                '2018-10-12',
                '2018-10-13',
                '2018-10-14',
                '2018-10-15',
                '2018-10-16',
                '2018-10-17'],
                dtype='datetime64[ns]', freq='D')}

        Returns
        -------
        self.__event_influenced_date : dict
        """
        if type(event_date) is not list:
            self.__raise_error(InvalidDateList,
                               details='event_date should be a list')
        try:
            event_date = pd.to_datetime(event_date)
        except ValueError:
            self.__raise_error(InvalidDateList,
                               details="Element in date list should in correct string form such as '%Y-%m-%d'")
        self.__event_date = event_date
        self.__event = event_name
        self.__event_influenced_date = self.__get_event_influenced_date()
        if display:
            return self.__event_influenced_date
        else:
            return "Event Fits Successfully"

    def get_index_effect(self):
        """
        Get the effect of the event on main index (including the mean return
        and rise probability)

        Parameters
        ----------

        Examples
        --------
        >> get_index_effect()
                    return	up_prob
        index
        上证50	-0.003689	0.166667
        上证综指	-0.004874	0.250000
        中小板指数	-0.007409	0.333333
        中证500	-0.007353	0.333333
        创业板指数	-0.008028	0.333333
        沪深500	-0.005041	0.333333
        深圳成指	-0.006799	0.250000

        Returns
        -------
        result : DataFrame
        """
        if self.__event_date is None or self.__event is None:
            self.__raise_error(NoEventDefined,
                               details='Please call the function fit() first')
        effect_df = pd.DataFrame()
        name = 'index'
        result = pd.DataFrame()
        for date in self.__event_influenced_date.keys():
            effect_period = self.__event_influenced_date[date]
            data = self.__data[name]
            data = data.loc[data.index.intersection(effect_period)]
            ret = data.groupby(name, as_index=False).agg({
                'return': 'mean',
                'volume': 'sum'
            })
            ret['date'] = date
            effect_df = effect_df.append(ret.set_index('date'))
            result = pd.DataFrame()
            for index, index_df in effect_df.groupby('index'):
                result.loc[index, 'return'] = index_df['return'].mean()
                result.loc[index, 'up_prob'] = sum(index_df['return'] >= 0) / \
                                               index_df.shape[0]
            result.index.name = 'index'
        return result

    def get_industry_effect(self, ascending=False, head=5):
        """
        Get the effect of the event on industry (including the mean return
        and rise probability)

        Parameters
        ----------
        ascending: boolean, default False
            Whether to sort the return column in an ascending way
        head: int, default 5
            the number of rows of the dataframe to return

        Examples
        --------
        >> get_industry_effect(method='return')
                    return	up_prob
        industry
        银行III	0.002723	0.583333
        石油开采III	0.001797	0.833333
        黄金III	0.001557	0.666667
        洗衣机III	0.001389	0.583333
        保险III	0.001299	0.583333

        Returns
        -------
        result : DataFrame
        """
        if self.__event_date is None or self.__event is None:
            self.__raise_error(NoEventDefined,
                               details='Please call the function fit() first')
        index = self.__data['index']
        index = index.loc[index['index'] == '上证综指']
        result = pd.DataFrame()
        effect_df = pd.DataFrame()
        name = 'industry'
        for date in self.__event_influenced_date.keys():
            effect_period = self.__event_influenced_date[date]
            data = self.__data[name]
            data = data.loc[data.index.intersection(effect_period)]
            ret = data.groupby('industry_name', as_index=False).agg({
                'return': 'mean',
                'volume': 'sum'
            })
            ret['date'] = date
            ret['return'] -= index.reindex(effect_period)['return'].mean()
            effect_df = effect_df.append(ret.set_index('date'))
            result = pd.DataFrame()
            for ind, index_df in effect_df.groupby('industry_name'):
                result.loc[ind, 'return'] = index_df['return'].mean()
                result.loc[ind, 'up_prob'] = sum(index_df['return'] >= 0) / \
                                             index_df.shape[0]
            result.index.name = 'industry'
            if ascending:
                result = result.loc[result['up_prob'] <= 0.5]

            else:
                result = result.loc[result['up_prob'] >= 0.5]
            result.sort_values(by='return', ascending=ascending,
                               inplace=True)
        return result.head(head)

    def get_stock_effect(self, industry=None, ascending=False, head=5):

        """
        Get the effect of the event on stock (including the mean return
        and rise probability)

        Parameters
        ----------
        industry: string
            the industry of stocks to be analyzed
        ascending: boolean, default False
            Whether to sort the return column in an ascending way
        head: int, default 5
            the number of rows of the dataframe to return

        Examples
        --------
        >> get_stock_effect(industry='银行III')
                        return	up_prob
        stock
        600926.XSHG	0.003148	1.000000
        601229.XSHG	0.003131	1.000000
        601009.XSHG	0.001737	0.583333
        600036.XSHG	0.001681	0.666667
        601169.XSHG	0.001548	0.583333

        Returns
        -------
        result : DataFrame
        """
        if self.__event_influenced_date is None:
            self.__raise_error(NoEventDefined,
                               details='Please call the function fit() first')
        if industry is None:
            industry = self.get_industry_effect().index[0]

        stock_ind = self.__data['stock_ind']
        stock_list = stock_ind.loc[stock_ind['industry_name'] == industry]
        stock_data = utility.get_stock_data(tuple(stock_list.stock.tolist()))
        stock_data.set_index('date', inplace=True)
        industry_data = self.__data['industry']
        industry_ret = industry_data.loc[
            industry_data['industry_name'] == industry]
        if industry_ret.empty:
            self.__raise_error(InvalidIndustryName,
                               details="Please check and retry with a correct industry name")

        effect_df = pd.DataFrame()
        result = pd.DataFrame()
        for date in self.__event_influenced_date.keys():
            effect_period = self.__event_influenced_date[date]
            # data = stock_data.loc[effect_period].dropna()
            data = stock_data.loc[stock_data.index.intersection(effect_period)]
            ret = data.groupby('stkcode', as_index=False).agg({
                'return': 'mean',
                'volume': 'sum'
            })
            ret['date'] = date
            ret['return'] -= industry_ret.reindex(effect_period)[
                'return'].mean()
            effect_df = effect_df.append(ret.set_index('date'))
            result = pd.DataFrame()
            for ind, index_df in effect_df.groupby('stkcode'):
                result.loc[ind, 'return'] = index_df['return'].mean()
                result.loc[ind, 'up_prob'] = sum(index_df['return'] >= 0) / \
                                             index_df.shape[0]
            result.index.name = 'stock'
            if ascending:
                result = result.loc[result['up_prob'] <= 0.5]
            else:
                result = result.loc[result['up_prob'] >= 0.5]
            result.sort_values(by='return', ascending=ascending, inplace=True)
        return result.head(head)

    def __compute_return(self, data, before, after):
        """
        compute the cumulative return for the data (stock data or industry data)
        during the time interval specified by the before and after argument
        and the event date

        Parameters
        ----------
        data: DataFrame
            the DataFrame of stock or industry
        before: int
            how many days before the event date
        after: int
            how many days after the event date

        Returns
        -------
        event_ret.mean().values : float
        """

        event_ret = pd.DataFrame()
        for date in self.__event_date:
            subset_range = pd.date_range(
                start=date - pd.Timedelta("{d} days".format(d=before)),
                end=date + pd.Timedelta("{d} days".format(d=after)))
            data_df = data.reindex(subset_range).dropna()
            if data_df.empty:
                break
            event_ret.loc[date, 'return'] = (data_df['return'] + 1).prod() - 1
        return event_ret.mean().values

    def get_stock_analysis(self, stock, before_periods=30, after_periods=30,
                           detail=True):
        """
        Get the best time for buying and selling the stock

        Parameters
        ----------
        stock: string
            the code of stock to be analyzed
        before_periods: int, default 30
            the periods before the event to buy stocks
        after_periods: int, default 30
            the periods after the event to sell stocks
        detail: boolean, default True
            Whether to return detailed result (for each different time interval)

        Examples
        --------
        >> get_stock_analysis(stock='600036.XSHG', detail=False)

        {
            'best_buy': 1,
            'best_sell': 9,
            'best_return': 0.03824388745185794,
            'ind_return': 0.01466740790957588,
            'all_period_detail': None
        }

        Returns
        -------
        dict
        """
        if self.__event_date is None:
            self.__raise_error(NoEventDefined,
                               details='Please call the function fit() first')
        stock_data = utility.get_stock_data(stock, list_bool=False)
        if stock_data is None or stock_data.empty:
            self.__raise_error(InvalidStockCode,
                               details="Please check and retry with a correct stock code")
        stock_data = stock_data.set_index('date')
        stock_ind = self.__data['stock_ind'].set_index('stock').loc[
            stock, 'industry_name']
        industry_data = self.__data['industry']
        industry_data = industry_data.loc[
            industry_data['industry_name'] == stock_ind]
        result = pd.DataFrame()
        count = 0
        for before in range(before_periods + 1):
            for after in range(after_periods + 1):
                count += 1
                result.loc[count, 'before'] = before
                result.loc[count, 'after'] = after
                result.loc[count, 'return'] = self.__compute_return(stock_data,
                                                                    before,
                                                                    after)
                result.loc[count, 'ind_ret'] = self.__compute_return(
                    industry_data, before, after)
        result.drop(1, inplace=True)
        result['before'] = result['before'].astype(int)
        result['after'] = result['after'].astype(int)
        return {
            'best_buy': int(result.loc[result['return'].idxmax(), 'before']),
            'best_sell': int(result.loc[result['return'].idxmax(), 'after']),
            'best_return': result.loc[result['return'].idxmax(), 'return'],
            'ind_return': result.loc[result['return'].idxmax(), 'ind_ret'],
            'all_period_detail': result.set_index(
                ['before', 'after']) if detail else None
        }


if __name__ == '__main__':
    pass
