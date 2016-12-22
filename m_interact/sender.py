#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

import json
import datetime

import tornado
import tornado.web

from tornado import gen
from tornado.httpclient import AsyncHTTPClient,HTTPRequest

from tornado.web import MissingArgumentError
from tornado.concurrent import run_on_executor

from concurrent.futures import ThreadPoolExecutor

from bson.objectid import ObjectId
import redis

from SOAPpy import SOAPProxy

from conf_util import ConfUtil
from utils.xmlGenerator import XMLGenerator
from utils.fileDownloader import FilesDownloader
from resourceses.resourceses import redis_pool


class UnSupportWebError(Exception):

    def __init__(self, web_str):
        self.web_str = web_str

    def __str__(self):
        return 'Web string %s is unsuported'%self.web_str

xmlGenerator = XMLGenerator()

class AllSender(tornado.web.RequestHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        self.write("Push all media is impossible")

MAX_WORKERS=4
class XXXSender(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    xmlyImgDownloader = FilesDownloader(ConfUtil.getXmlyImgDir())
    xmlyAudioDownloader = FilesDownloader(ConfUtil.getXmlyAudioDir())
    qtImgDownloader = FilesDownloader(ConfUtil.getQtImgDir())
    qtAudioDownloader = FilesDownloader(ConfUtil.getQtAudioDir())
    klImgDownloader = FilesDownloader(ConfUtil.getKlImgDir())
    klAudioDownloader = FilesDownloader(ConfUtil.getKlAudioDir())

    proxy =SOAPProxy(ConfUtil.getCnrUri())

    redis = redis.Redis(connection_pool=redis_pool)

    def initialize(self, collection, web_str):
        self.collection = collection
        self.web_str = web_str

    @gen.coroutine
    def get(self, *args, **kwargs):
        user = {"Name":"Pradeep", "Company":"SCTL", "Address":"Mumbai", "Location":"RCP"}
        self.redis.hmset("foiiio",user)
        cache = self.redis.hgetall("foiiio")
        self.write(cache)

    # 推送数据到cnr的索贝接口
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        _ids = data.get('_ids',None)
        force_push = data.get('force_push',False)
        if not _ids:
            raise MissingArgumentError("_ids")
        coll = self.application.db[self.collection]
        if force_push:
            audios = yield [coll.find_one({
                "_id":ObjectId(_id)
            }) for _id in _ids]
        else:
            audios = yield [coll.find_one({
                "_id":ObjectId(_id),
                "sendToCNRTime":None
            }) for _id in _ids]
        # 如果对应的audio与媒体文件没有被下载，那么下载对应的audio与媒体文件
        audiosInfo = None
        imgsInfo = None
        if self.web_str == 'kl':
            # 因为kl网站挂掉了所以暂时不提供kl网站下载
            raise UnSupportWebError(self.web_str)
        elif self.web_str == 'xmly':
            # 因为取消掉媒体文件下载进程，所以所有媒体文件下载都在这里
            audios_url = [audio.get("play_path",None) for audio in audios]
            imgs_url = [audio.get("cover_url_142",None) for audio in audios]
            audiosInfo = yield [self.xmlyAudioDownloader.download_file(url) for url in audios_url]
            imgsInfo = yield [self.xmlyImgDownloader.download_file(url) for url in imgs_url]

        elif self.web_str == 'qt':
            audios_url = [audio.get("playUrl") for audio in audios]
            audiosInfo = yield [self.qtAudioDownloader.download_file(url) for url in audios_url]

            # 因为爬虫没有获得img url，所以imgs 都为空
            imgsInfo = [None for audio in audios]
        else:
            raise UnSupportWebError(self.web_str)

        audiosInfo = zip(audios,audiosInfo,imgsInfo)

        xmls = [xmlGenerator.getXMLContentFromAudio(self.web_str,audioInfo) for audioInfo in audiosInfo if audiosInfo[0]]
        resps = yield [self.sendXMLToCNR(xml) for xml in xmls]
        # 将推送到cnr 的时间设置到数据库中
        yield [coll.update(
            {"_id":audio["_id"]},
            {
                "$set":{
                    "sendToCNRTime":datetime.datetime.now()
                }
            }
        ) for audio in audios]
        self.write({"audios":[audio.get('album_title') for audio in audios],
                    "resps":['success' if resp else 'fault' for resp in resps],
                    "request_push_count":len(_ids),
                    "real_push_count":len(xmls),
                    "force_push":force_push,
                    })

    @run_on_executor
    def sendXMLToCNR(self, xml):
        '''
        将xml 内容推送到cnr
        :param xml:
        :return:
        '''
        resp = self.proxy.mpccommit(
            strInput = xml
        )
        return resp
