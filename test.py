#coding=utf-8
__author__ = 'xiyuanbupt'
import unittest
#from tests.example import TestFoo
#from tests.testFileDownloader import TestFileDownloader
#from tests.testSender import TestSender

import requests
import urlparse
import json
import pprint
import time
import datetime

url_base = 'http://localhost:8000'


def test_sender():
    print u'测试推送xmly音频文件，推送两个文件并且未强制推送'
    url = urlparse.urljoin(url_base,'api/sender/vod/xmly')
    body = {
        "post_address":"http://httpbin.org/post",
        "_ids":["571a2e0de1382377590c23e7","571a2e0ce1382377590c23e6"],
        "force_push":True
    }
    res = requests.post(url,json=body)
    print(u'测试的结果是: ')
    pprint.pprint(json.loads(res.text))
    assert res.ok == True

    print u''
    print u'测试推送qt音频文件与图片文件，推送两个文件并强制推送'
    url = urlparse.urljoin(url_base,'api/sender/vod/qt')
    body = {
        "post_address":"http://httpbin.org/post",
        "_ids":["582568ef0e640d11bb38329c","582568ef0e640d11bb38329b","582568ef0e640d11bb38329a"],
        "force_push":True
    }
    res = requests.post(url,json=body)
    print(u'测试的结果是: ')
    pprint.pprint(json.loads(res.text))
    assert res.ok == True

def test_stop_runner():
    print u'测试爬虫启停'
    url = urlparse.urljoin(url_base,'api/xmly/full')
    print u'获得xmly全量状态'

    res = requests.get(url)
    pprint.pprint(res.text)

    assert json.loads(res.text).get('statename') == 'STOPPED'

    print u'启动'


class TestApi(unittest.TestCase):

    def testSender(self):
        print u'测试推送xmly音频文件，推送两个文件并且未强制推送'
        url = urlparse.urljoin(url_base,'api/sender/vod/xmly')
        body = {
            "post_address":"http://httpbin.org/post",
            "_ids":["571a2e0de1382377590c23e7","571a2e0ce1382377590c23e6"],
            "force_push":True
        }
        res = requests.post(url,json=body)
        self.assertTrue(res.ok)

        url = urlparse.urljoin(url_base,'api/sender/vod/qt')
        body = {
            "post_address":"http://httpbin.org/post",
            "_ids":["582568ef0e640d11bb38329c","582568ef0e640d11bb38329b","582568ef0e640d11bb38329a"],
            "force_push":True
        }
        res = requests.post(url,json=body)
        print(u'测试的结果是: ')
        pprint.pprint(json.loads(res.text))
        self.assertTrue(res.ok)

    def testXMLYFullStopRunner(self):

        print u'测试xmly全量的启停'
        url = urlparse.urljoin(url_base,'api/xmly/full')
        res = requests.get(url)
        self.assertEqual(
            json.loads(res.text).get('statename'),
            'STOPPED'
        )


    def testXMLYTopnStopRunner(self):

        print u'测试topn启动，首先停止爬虫'
        url = urlparse.urljoin(url_base,'api/xmly/topn')
        before = datetime.datetime.now()
        print requests.delete(url).text
        after = datetime.datetime.now()
        print u'停止爬虫一共花费:'
        print  (after-before).seconds

        print u'获得topn当前状态,确定是停止的'
        res = requests.get(url)
        print res.text
        self.assertEqual(
            json.loads(res.text).get('state'),
            100
        )

        print u'启动xmly topn'
        res = requests.post(
            url,
            json={
                "topn_n":12,
                "urls":[]
            }
        )
        print res.text
        time.sleep(2)
        res = requests.get(url)
        self.assertEqual(
            json.loads(res.text).get('statename'),
            'RUNNING'
        )

        print u'最后停止爬虫'
        before = datetime.datetime.now()
        print requests.delete(url).text
        after = datetime.datetime.now()
        print u'最后停止爬虫一共花费:'
        print  (after-before).seconds


if __name__ == "__main__":
    unittest.main()
    pass
    # unittest.main()
    # sudo docker run --name mongo_instance_001 -d my/repo --noprealloc --smallfiles


