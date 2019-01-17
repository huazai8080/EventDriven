# EventDriven
This package is designed to automate some important steps when doing research on the event-driven effect on stocks.

该系统提供标准化的接口，可用来研究事件对大盘、行业以及个股的影响。该库提供一系列与事件驱动相关的方法，包括得到事件的影响时间范围，事件影响时间范围内大盘的涨跌分析，以及该事件对不同行业涨跌幅和交易量的影响，并挖掘与该事件相关程度最高的个股并提出投资建议。该接口可供研究人员撰写研究报告参考。

## 调用说明

1. 打开百度的首页，登录后，将百度首页的cookie复制后，粘贴到config.py中的COOKIES对象中
2. 导入event_driven.py文件，并创建EventDriven类的实例。\
from event_driven import EventDriven \
event = EventDriven() \
然后可以通过实例对象调用一系列接口，具体可参考demo.py\
接口调用文档说明：https://www.showdoc.cc/EventDriven?page_id=1441598469644058
