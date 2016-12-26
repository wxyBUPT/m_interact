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

from SOAPpy import SOAPProxy

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
    pprint.pprint(json.loads(res.text))
    assert res.ok == True

def test_stop_runner():
    url = urlparse.urljoin(url_base,'api/xmly/full')

    res = requests.get(url)
    pprint.pprint(res.text)

    assert json.loads(res.text).get('statename') == 'STOPPED'



class TestApi(unittest.TestCase):

    def testSender(self):
        url = urlparse.urljoin(url_base,'api/sender/vod/xmly')
        body = {
            "post_address":"http://localhost:8080/",
            "_ids":["571a2e0de1382377590c23e7","571a2e0ce1382377590c23e6"],
            "force_push":True
        }
        res = requests.post(url,json=body)
        self.assertTrue(res.ok)

        url = urlparse.urljoin(url_base,'api/sender/vod/qt')
        body = {
            "post_address":"http://localhost:8080/",
            "_ids":["582568ef0e640d11bb38329c","582568ef0e640d11bb38329b","582568ef0e640d11bb38329a"],
            "force_push":True
        }
        res = requests.post(url,json=body)
        pprint.pprint(json.loads(res.text))
        self.assertTrue(res.ok)

    def testXMLYFullStopRunner(self):

        url = urlparse.urljoin(url_base,'api/xmly/full')
        res = requests.get(url)
        self.assertEqual(
            json.loads(res.text).get('statename'),
            'STOPPED'
        )


    def testXMLYTopnStopRunner(self):

        url = urlparse.urljoin(url_base,'api/xmly/topn')
        before = datetime.datetime.now()
        print requests.delete(url).text
        after = datetime.datetime.now()
        print  (after-before).seconds

        res = requests.get(url)
        print res.text
        self.assertEqual(
            json.loads(res.text).get('state'),
            100
        )

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

        before = datetime.datetime.now()
        print requests.delete(url).text
        after = datetime.datetime.now()
        print  (after-before).seconds

def test_cnr_api():
    namespace = "http://10.20.30.21:8088/"
    url = "http://10.20.30.21:8088/"
    proxy = SOAPProxy(url, namespace)
    proxy.config.debug = 1
    with open('./m_interact/templates/examle.xml') as f:
        strInput = f.readall()
        proxy.mpccommit(
            strInput = strInput
        )
    proxy.mpccommit(
        strInput = "foo"
    )



if __name__ == "__main__":
    unittest.main()
    pass
    # unittest.main()
    # sudo docker run --name mongo_instance_001 -d my/repo --noprealloc --smallfiles


