from event_driven import EventDriven

if __name__ == "__main__":
    event = EventDriven()

    # 获取降准事件的影响时间范围
    print(event.fit(event.rrr_date, '降准', display=True))

    # 获取降准事件对大盘的影响
    print(event.get_index_effect())

    # 获取降准事件对不同行业的影响（按收益率从低到高排序，返回前5的行业）
    print(event.get_industry_effect(ascending=False, head=5))

    # 获取降准事件对某一个行业所有股票的影响（按收益率从低到高排序，返回前5的股票）
    print(event.get_stock_effect(industry='银行III'))

    # 获取针对降准事件，某一支股票的最优买入卖出时机
    print(event.get_stock_analysis(stock='600036.XSHG', detail=False))




