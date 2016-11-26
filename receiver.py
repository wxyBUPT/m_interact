#coding=utf-8
__author__ = 'xiyuanbupt'

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from motor.motor_tornado import MotorClient
from tornado.web import URLSpec as url

from tornado.options import define,options
define("port",default=8000,help=u'接收请求的端口，默认为8000',type=int)

from m_interact.feedBack import FeedBack,HandleQTRe,HandleKLRe,HandleXMLYRe,ViewSummary
from m_interact.sender import XXXSender,AllSender
from m_interact.crawlerManager import XXXManager,QtTopnManager,XMLYTopnManager
from conf_util import ConfUtil

#在urlpatterns 中添加新的路由
urlpatterns = [
    (r'/infoCrawler',FeedBack),
    (r'/toCNR/xmly/(\w+)',HandleXMLYRe),
    (r'/toCNR/kl/(\w+)',HandleKLRe),
    (r'/toCNR/qt/(\w+)',HandleQTRe),
    #对内的统计页面，资源整体情况描述
    (r'/toStatistic/summary/',ViewSummary),
    # xmly 数据推送
    url(r'/api/sender/vod/xmly',XXXSender,dict(collection = ConfUtil.getXMLYAudioCollectionName(),
                                               web_str='xmly'
                                               )),
    url(r'/api/sender/vod/qt',XXXSender,dict(collection = ConfUtil.getQTAudioCollectionName(),
                                             web_str = 'qt'
                                             )),
    url(r'/api/sender/vod/kl',XXXSender,dict(
        collection = ConfUtil.getKLAudioCollectionName(),
        web_str = 'kl'
    )),

    url(r'/api/xmly/full', XXXManager, dict(
        process_name = ConfUtil.xmlyFullProcessName()
    )),

    url(r'/api/qt/full', XXXManager, dict(
        process_name = ConfUtil.qtFullProcessName()
    )),

    url(r'/api/xmly/increment', XXXManager, dict(
        process_name = ConfUtil.xmlyIncreProcessName()
    )),

    url(r'/api/kl/increment', XXXManager, dict(
        process_name = ConfUtil.klIncreProcessName()
    )),

    url(r'/api/qt/increment', XXXManager, dict(
        process_name = ConfUtil.qtIncreProcessName()
    )),

    url(r'/api/kl/full', XXXManager, dict(
        process_name = ConfUtil.klFullProcessName()
    )),

    url(r'/api/qt/topn', QtTopnManager, dict(
        process_name = ConfUtil.qtTopnProcessName()
    )),

    url(r'/api/xmly/topn', XMLYTopnManager, dict(
        process_name = ConfUtil.xmlyTopnProcessName()
    )),

    url(r'/api/sender/vod/all',AllSender)

]


class Application(tornado.web.Application):
    def __init__(self):
        handlers = urlpatterns
        conn = MotorClient(ConfUtil.getMongoIP(),ConfUtil.getMongoPort())
        self.db = conn[ConfUtil.getDBName()]
        settings = dict(
            template_path = ConfUtil.getTemplatePath(),
            static_path = ConfUtil.getStaticPath(),
            debug = True,
        )
        tornado.web.Application.__init__(self,handlers=handlers,**settings)

def make_app():
    return Application()

def run():
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    run()