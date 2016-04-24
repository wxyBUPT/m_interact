#coding=utf-8
from __future__ import absolute_import
__author__ = 'xiyuanbupt'
import datetime
import requests
import logging
import logging.config
logging.config.fileConfig('./logger.ini')
from xml.etree.ElementTree import Element
from jinja2 import Environment,PackageLoader
from pymongo import MongoClient
import requests

from conf_util import ConfUtil
env = Environment(loader=PackageLoader('m_interact','templates'))
'''
用于向接口中推送数据，每天会在固定的时间启动一个 sender 进程，用来推送当前的数据
'''
client = MongoClient(ConfUtil.getMongoIP(),ConfUtil.getMongoPort())
db = client[ConfUtil.getDBName()]


class Sender:
    klAudio = db[ConfUtil.getKLAudioCollectionName()]
    xmlyAudio = db[ConfUtil.getXMLYAudioCollectionName()]
    qtAudio = db[ConfUtil.getQTAudioCollectionName()]
    template = env.get_template('sendTemp.xml')
    soapTargetUri = ConfUtil.getSoapTargetUri()

    def __init__(self):
        pass

    def useJinja(self):
        template = env.get_template('sendTemp.xml')
        return template.render(PGMGUID = 'wwww')

    #从数据库中读取所有未被推送到cnr 并且媒体文件已经被下载的数据项
    def getXMLYAudioNotInCNRWithFile(self):
        '''
        获得所有未被推送到CNR 但是媒体文件已经被下载的 audio
        '''
        with self.xmlyAudio.find(
            {
                "sendToCNRTime":None,
                "audioDownloadDir":{"$ne":None}
            }
        ) as cursor:
            for audio in cursor:
                yield audio

    def getKLAudioNotInCNRWithFile(self):
        '''
        获得所有未被推送到CNR 但是媒体文件已经被下载的audio
        '''
        with self.klAudio.find(
            {
                "sendToCNRTime":None,
                "audioDownloadDir":{"$ne":None}
            }
        ) as cursor:
            for audio in cursor:
                yield audio

    def getQTAudioNotInCNRWithFile(self):
        '''
        获得未被推送到cnr 但是媒体文件已经被下载的audio，qt 网站
        :return:
        '''
        with self.qtAudio.find(
                {
                    "sendToCNRTime":None,
                    "audioDownloadDir":{"$ne":None}
                }
        ) as cursor:
            for audio in cursor:
                yield  audio


    def getXMLContentFromAudio(self,sourceWeb,audio):
        '''
        从audio 中获得 xml 内容
        函数会根据 sourceWeb 的不同来决定推送的逻辑
        sourceWeb 为 kl xmly 或者 qt
        audio 为直接从 数据库中取到的对应网站audio 的字典格式
        '''
        now = datetime.datetime.now()
        RequestID = audio.get('uuid',None)
        RequestTime = now.strftime("%Y-%m-%d %H:%M:%S")
        TaskGUID = audio.get('uuid',None)
        TaskName = audio.get('album_title',None)
        PutinTime = now.strftime("%Y-%m-%d %H:%M:%S")
        uuid = audio.get('uuid',None)
        SoapTargetUri = self.soapTargetUri.format(
            sourceWeb = sourceWeb,uuid = uuid
        )
        PGMNAME = TaskName
        PGMGUID = audio.get('uuid',None)
        Title = TaskName
        #如下代码之后需要重构，已经将sourceWeb 写死在，故并不通用
        if sourceWeb == 'kl':
            CATALOGNAME = u'考拉fm\点播\{category}\{album}'.format(
                category = audio.get('category_title',u'未知'),
                album = audio.get('album_title',u'未知')
            )
            CreatorName = audio.get('uploaderName',u'北邮爬虫').strip()
            PgmNote = audio.get('fullDescs',u'描述未知')
            FileName = audio.get('audioDownloadDir',None)
        elif sourceWeb == 'xmly':
            CATALOGNAME = u'喜马拉雅fm\点播\{category}\{album}'.format(
                category = audio.get('category_title',u'未知'),
                album = audio.get('album_title',u'未知')
            )
            CreatorName = audio.get('uploadUserName',u'北邮爬虫').strip()
            PgmNote = audio.get('intro',u'描述未知')
            FileName = audio.get('audioDownloadDir',None)

        elif sourceWeb == 'qt':
            CATALOGNAME = u'蜻蜓fm\点播\{category}\{album}'.format(
                category = audio.get('category_title',u'未知类别'),
                album = audio.get('album_title',u'未知专辑')
            )
            CreatorName = u'蜻蜓fm，作者未知'
            PgmNote = audio.get('audioName',u'描述未知')
            FileName = audio.get('audioDownloadDir',None)
        else:
            print u'未知sourceWeb'
        xmlContent = self.template.render(
            RequestID = RequestID,
            RequestTime = RequestTime,
            TaskGUID = TaskGUID,
            PutinTime = PutinTime,
            uuid = uuid,
            SoapTargetUri = SoapTargetUri,
            PGMNAME = PGMNAME,
            PGMGUID = PGMGUID,
            Title = Title,
            CATALOGNAME = CATALOGNAME,
            CreatorName = CreatorName,
            PgmNote = PgmNote,
            FileName = FileName,
            TaskName = TaskName,
            firstplaytime = None,
            broadstarttime = None,
            broadendtime = None
        )

        return xmlContent

    def sendXMLToCNR(self,xml):
        '''
        将xml 内容推送到cnr
        :param xml:
        :return:
        '''
        headers = {'Content-Type':'application/xml'}
        res = requests.post(ConfUtil.getCnrUri(),data=xml.encode('utf-8'),
                            headers = headers)
        return res

    def getAudioPutToCNR(self,count = 10):
        '''
        冷启动，或者平时使用，向cnr 发送当前数据库中有媒体文件但是未被发送到cnr 的数据
        执行获得所有未被推送到cnr ，并且文件已经被下载到本地种的audio 并将其推送至cnr
        并更改标志位
        :param count 为本次期望发送到cnr 最大的音频数量,默认为10，生产环境中需要更改
        '''
        logger = logging.getLogger('sender')
        #每个网站推送相同的数据量
        count = count/3
        xcount , qcount , kcount = count,count,count
        xmlyAudios = self.getXMLYAudioNotInCNRWithFile()
        for xmlyAudio in xmlyAudios:
            xcount -= 1
            if xcount < 0:
                break
            xmlContent = self.getXMLContentFromAudio('xmly',xmlyAudio)
            resp = self.sendXMLToCNR(xmlContent)
            #需要添加根据返回的状态判断相关信息
            if True:
                logger.info(
                    u'send xmlyAudio uuid - {0}'.format(
                        xmlyAudio['uuid']
                    )
                )

        klAudios = self.getKLAudioNotInCNRWithFile()
        for klAudio in klAudios:
            kcount -= 1
            if kcount < 0:
                break
            xmlContent = self.getXMLContentFromAudio('kl',klAudio)
            resp = self.sendXMLToCNR(xmlContent)
            if True:
                logger.info(
                    u'send klAudio uuid - {0}'.format(
                        klAudio['uuid']
                    )
                )
        qtAudios = self.getQTAudioNotInCNRWithFile()
        for qtAudio in qtAudios:
            qcount -= 1
            if qcount < 0:
                break
            xmlContent = self.getXMLContentFromAudio('qt',qtAudio)
            resp = self.sendXMLToCNR(xmlContent)
            if True:
                logger.info(
                    u'send qtAudio uuid - {0}'.format(
                        qtAudio['uuid']
                    )
                )

#   def dict_to_xml(self,tag,d):
#       '''
#       Trun a simple dict of key/value pairs into XML
#       :param tag:
#       :param d:
#       :return:
#       '''
#       elem = Element(tag)
#       for key,val in d.items():
#           if type(val) == type({}):
#               elem.append(self.dict_to_xml(key,val))
#           else:
#               child = Element(key)
#               child.text = str(val)
#               elem.append(child)
#       return elem


