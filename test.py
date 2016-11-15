#coding=utf-8
__author__ = 'xiyuanbupt'
import unittest
from sender import  Sender
from tests.example import TestFoo
from tests.testFileDownloader import TestFileDownloader

class TestSender(unittest.TestCase):

    sender = Sender()
    def testGetXMLYAudioNotInCNRWiFile(self):
        audios = self.sender.getXMLYAudioNotInCNRWithFile()
        audio = audios.next()
        self.assertIsNotNone(audio)

    def testKLAudioNotInCNRWithFile(self):
        '''
        测试获得未被推送到
        :return:
        '''
        audios = self.sender.getKLAudioNotInCNRWithFile()
        audio = audios.next()
        self.assertIsNotNone(audio)

    def testQTAudioNotINCNRWithFile(self):
        '''
        audios = self.sender.getQTAudioNotInCNRWithFile()
        audio = audios.next()
        self.assertIsNotNone(
            audio['audioDownloadDir']
        )
        self.assertIsNone(
            audio['sendToCNRTime']
        )
        '''
        pass

    def testGetXMLContentFromAudio(self):
        '''
        测试从audio 信息中获得xml 内容
        :return:
        '''
        '''
        xmlyAudio = self.sender.getXMLYAudioNotInCNRWithFile().next()
        klAudio = self.sender.getKLAudioNotInCNRWithFile().next()
        qtAudio = self.sender.getQTAudioNotInCNRWithFile().next()
        self.assertIsNotNone(xmlyAudio)
        self.assertIsNotNone(klAudio)
        self.assertIsNotNone(qtAudio)
        '''
        pass

    def testLogger(self):
        import logging
        logger = logging.getLogger('sender')
        logger.error(u'这是一条测试日志')

    def testSendXMLToCNR(self):
        xmlyAudio = self.sender.getXMLYAudioNotInCNRWithFile().next()
        xml = self.sender.getXMLContentFromAudio('xmly',xmlyAudio)
        resp = self.sender.sendXMLToCNR(xml).text
        import json
        resp = json.loads(resp,encoding='utf-8')
        self.assertIsNotNone(resp['data'])
        # print resp['data']

    def testGetAudioPutToCNR(self):
        self.sender.getAudioPutToCNR(3)


if __name__ == "__main__":
    unittest.main()

