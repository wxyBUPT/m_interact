#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

import datetime
from os import path
import os

from jinja2 import Environment,PackageLoader
from conf_util import ConfUtil

class XMLGenerator:

    # 转码服务器共享盘挂载的路径
    transcoding_mount = 'H:'
    # 爬虫服务器共享盘挂载的路径
    my_mount = '/var/crawler/cnr_shares'

    template = Environment(loader=PackageLoader('m_interact','templates')).get_template(
        'sendTemp.xml'
    )
    soapTargetUri = ConfUtil.getSoapTargetUri()

    def __init__(self):
        pass

    def getXMLContentFromAudio(self,sourceWeb,audioInfo):
        '''
        从audio 中获得 xml 内容
        函数会根据 sourceWeb 的不同来决定推送的逻辑
        sourceWeb 为 kl xmly 或者 qt
        audio 为直接从 数据库中取到的对应网站audio 的字典格式
        '''
        audio = audioInfo[0]
        audioFile = audioInfo[1]
        imgFile = audioInfo[2]

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
                category = audio.get('category_title',u'未知').strip(),
                album = audio.get('album_title',u'未知').strip()
            )
            CreatorName = audio.get('uploaderName',u'Crawler').strip()
            PgmNote = audio.get('fullDescs',u'描述未知').strip()
            AudioFileName = audioFile.get('path',None) if audioFile else None
            ImgFileName = imgFile.get('path',None) if imgFile else None
        elif sourceWeb == 'xmly':
            CATALOGNAME = u'喜马拉雅fm\点播\{category}\{album}'.format(
                category = audio.get('category_title',u'未知').strip(),
                album = audio.get('album_title',u'未知').strip()
            )
            CreatorName = audio.get('uploadUserName',u'Crawler').strip()
            PgmNote = audio.get('intro',u'描述未知')
            AudioFileName = audioFile.get('path',None) if audioFile else None
            ImgFileName = imgFile.get('path',None) if imgFile else None
        elif sourceWeb == 'qt':
            CATALOGNAME = u'蜻蜓fm\点播\{category}\{album}'.format(
                category = audio.get('category_title',u'未知类别').strip(),
                album = audio.get('album_title',u'未知专辑').strip()
            )
            CreatorName = u'蜻蜓fm，作者未知'
            PgmNote = audio.get('audioName',u'描述未知')
            AudioFileName = audioFile.get('path',None) if audioFile else None
            ImgFileName = imgFile.get('path',None) if imgFile else None
        else:
            print u'未知sourceWeb'
        AudioFileName = changePathStyle(AudioFileName)
        ImgFileName = changePathStyle(ImgFileName)
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
            AudioFileName = self.transcoding_mount + AudioFileName,
            ImgFileName = (self.transcoding_mount + ImgFileName) if ImgFileName else None,
            TaskName = TaskName,
            firstplaytime = None,
            broadstarttime = None,
            broadendtime = None
        )

        return xmlContent

    # 将爬虫爬取的文件路径转换为转码服务器挂载的路径
my_mount = '/var/crawler/cnr_shares'
def changePathStyle( filePath):
    if not filePath:
        return filePath
    if filePath.startwith(my_mount):
        filePath = filePath[len(my_mount):]
    paths = filePath.split('/')
    filePath = '\\'.join(paths)
    return filePath

if __name__ == "__main__":
    changePathStyle('/var/crawler/cnr_shares/m4a/2016/12/26/e19af8357.m4a')
