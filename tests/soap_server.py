#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com
import SOAPpy
def hello(strInput):

    return strInput+ "Hello WOrld"

def mpccommit(strInput):

    return strInput + "success"

server = SOAPpy.SOAPServer(("localhost", 8080))
server.registerFunction(hello)
server.registerFunction(mpccommit)

server.serve_forever()

