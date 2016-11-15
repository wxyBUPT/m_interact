#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com
from tornado.testing import AsyncTestCase
from tornado.httpclient import AsyncHTTPClient,HTTPClient


class TestFileDownloader(AsyncTestCase):

    def testDownloadFile(self):
        client = HTTPClient()
        response = client.fetch("http://audio.xmcdn.com/group11/M00/37/80/wKgDbVWWnmDgH23vAFlLABTtPbA323.m4a")
        print(response.body)

