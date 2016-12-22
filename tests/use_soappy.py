#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

from SOAPpy import SOAPProxy
import datetime

date=datetime.datetime.now()
namespace ="http://web.cbr.ru/"
url = "http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx"
server = SOAPProxy(url,namespace)
print (date)
server.GetCursOnDate(date)
