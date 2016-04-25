#coding=utf-8
__author__ = 'xiyuanbupt'
import ConfigParser

cf = ConfigParser.ConfigParser()

cf.read("global.ini")

class ConfUtil:

    @classmethod
    def getDBName(cls):
        return cf.get('db','name')

    @classmethod
    def getXMLYAlbumCollectionName(cls):
        return cf.get('collections','xmly_album')

    @classmethod
    def getXMLYCategoryCollectionName(cls):
        return cf.get('collections','xmly_category')

    @classmethod
    def getKLAlbumCollectionName(cls):
        return cf.get('collections','kl_album')

    @classmethod
    def getKLCategoryCollectionName(cls):
        return cf.get('collections','kl_category')

    @classmethod
    def getQTAlbumCollectionName(cls):
        return cf.get('collections','qt_item')

    @classmethod
    def getMongoIP(cls):
        return cf.get('mongo','ip')

    @classmethod
    def getMongoPort(cls):
        return cf.getint('mongo','port')

    @classmethod
    def getCrontabDbCollectionName(cls):
        '''
        获得定期执行的脚本保存结果的 collection 名称
        :return:
        '''
        return cf.get('collections','crontab')

    @classmethod
    def getXMLYAudioCollectionName(cls):
        '''
        获得存储xmly 所有audio 信息的collection
        :return:
        '''
        return cf.get('collections','xmly_audio')

    @classmethod
    def getKLAudioCollectionName(cls):
        return cf.get('collections','kl_audio')

    @classmethod
    def getQTAudioCollectionName(cls):
        return cf.get('collections','qt_audio')

    @classmethod
    def getSoapTargetUri(cls):
        '''
        获得接收 从cnr 回调的地址
        :return:
        '''
        return cf.get('cnr','soaptargeturi')

    @classmethod
    def getCrontabResultCollectionName(cls):
        return cf.get('collections','crontab')

    @classmethod
    def getCnrUri(cls):
        '''
        获得将音频数据推送至cnr 的地址
        :return:
        '''
        return cf.get('cnr','uri')

    @classmethod
    def getCnrSendCountOnce(cls):
        '''
        获得一次推送到cnr 中audio 的数目
        :return:
        '''
        return cf.getint('cnr','sendCountOnce')
