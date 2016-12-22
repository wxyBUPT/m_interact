#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

import SOAPpy
proxy = SOAPpy.SOAPProxy("http://localhost:8080/")
proxy.config.debug = 1

print proxy.hello(strInput = 'wang')


