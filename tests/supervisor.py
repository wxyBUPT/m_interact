#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

import xmlrpclib

server = xmlrpclib.Server("http://user:123@114.112.103.33:9001/RPC2")

print server.supervisor.getState()