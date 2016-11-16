#coding=utf-8
__author__ = 'xiyuanbupt'
import ConfigParser
import os.path

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

    @classmethod
    def getTemplatePath(cls):
        path = cf.get('file','template_path')
        return path if path.startswith('/') else os.path.abspath(path)

    @classmethod
    def getStaticPath(cls):
        path = cf.get('file','static_path')
        return path if path.startswith('/') else os.path.abspath(path)

    @classmethod
    def getSleepSecAgterPush(cls):
        return cf.getint('cnr','sleepSecAfterSend')

    @classmethod
    def getSendThreadCount(cls):
        return cf.getint('cnr','sendThreadCount')

    @classmethod
    def getXmlyAudioDir(cls):
        return cf.get('download', 'xmly_audio')

    @classmethod
    def getXmlyImgDir(cls):
        return cf.get('download', 'xmly_img')

    @classmethod
    def getQtAudioDir(cls):
        return cf.get('download', 'qt_audio')

    @classmethod
    def getQtImgDir(cls):
        return cf.get('download','qt_img')

    @classmethod
    def getKlAudioDir(cls):
        return cf.get('download','kl_audio')

    @classmethod
    def getKlImgDir(cls):
        return cf.get('download', 'kl_img')

    @classmethod
    def getRedisHost(cls):
        return cf.get('redis', 'host')

    @classmethod
    def getRedisPort(cls):
        return cf.get('redis', 'port')

    @classmethod
    def getRedisDb(cls):
        return cf.get('redis', 'db')

    @classmethod
    def getTranscodServerHost(cls):
        return cf.get('transcoding', 'host')

    @classmethod
    def getTranscodServerUserNmae(cls):
        return cf.get('transcoding', 'user')

    @classmethod
    def getTranscodeServerUserPass(cls):
        return cf.get('transcoding', 'password')

    @classmethod
    def getTranscodeServerM4aDir(cls):
        return cf.get('transcoding', 'm4a_dir')

    @classmethod
    def getTranscodeServerJpgDir(cls):
        return cf.get('transcoding', 'jpg_dir')

    @classmethod
    def getSupervisorUri(cls):
        return cf.get('supervisor','uri')

    @classmethod
    def xmlyTopnProcessName(cls):
        return cf.get('supervisor','xmly_topn')

    @classmethod
    def klTopnProcessName(cls):
        return cf.get('supervisor','kl_topn')

    @classmethod
    def klFullProcessName(cls):
        return cf.get('supervisor','kl_full')

    @classmethod
    def xmlyFullProcessName(cls):
        return cf.get('supervisor','xmly_full')

    @classmethod
    def qtTopnProcessName(cls):
        return cf.get('supervisor', 'qt_topn')

    @classmethod
    def qtFullProcessName(cls):
        return cf.get('supervisor', 'qt_full')

    @classmethod
    def qtIncreProcessName(cls):
        return cf.get('supervisor', 'qt_increment')

    @classmethod
    def xmlyIncreProcessName(cls):
        return  cf.get('supervisor', 'xmly_increment')

    @classmethod
    def klIncreProcessName(cls):
        return cf.get('supervisor', 'kl_increment')

    @classmethod
    def xmly_topn_n_key(cls):
        return cf.get('xmly','topn_key')

    @classmethod
    def xmly_topn_table_key(cls):
        return cf.get('xmly', 'topn_table')
