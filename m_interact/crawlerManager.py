#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

u'''
负责管理爬虫的启停
'''
import xmlrpclib
import json
import redis
import datetime

from concurrent.futures import ThreadPoolExecutor
import tornado.web
from tornado import gen
from tornado.concurrent import run_on_executor

from conf_util import ConfUtil
from resourceses.resourceses import redis_pool

MAX_WORKERS=4

class XXXManager(tornado.web.RequestHandler):
    '''
    处理爬虫启停与状态
    '''
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    server = xmlrpclib.Server(ConfUtil.getSupervisorUri())
    supervisor = server.supervisor
    status_del_tags = [
        'group', 'pid', 'stderr_logfile', 'stdout_logfile',
        'logfile', 'spawnerr'
    ]


    def initialize(self, process_name):
        self.process_name = process_name

    @run_on_executor
    def get_process_info(self,process_name):
        status = self.supervisor.getProcessInfo(process_name)
        try:
            for key in self.status_del_tags:
                del(status[key])
        except Exception as e:
            pass
        return status

    @run_on_executor
    def stop_process(self, process_name):
        '''
        向进程发送Ctrl-C 命令
        :param process_name:
        :return:
        '''
        self.supervisor.signalProcess(process_name, '2')

    @run_on_executor
    def force_stop_process(self, process_name):
        '''
        强制停止进程
        :param process_name:
        :return:
        '''
        self.supervisor.stopProcess(process_name)

    @run_on_executor
    def direct_start_process(self, process_name):
        '''
        开始执行进程，对于互相间没有交互的
        :param process_name:
        :return:
        '''
        self.supervisor.startProcess(process_name)

    @gen.coroutine
    def get(self, *args, **kwargs):
        '''
        获得爬虫状态
        :param args:
        :param kwargs:
        :return:
        '''
        status = yield self.get_process_info(self.process_name)
        self.write(status)

    @gen.coroutine
    def post(self, *args, **kwargs):
        '''
        控制爬虫启停，只针对无交互的爬虫进程
        :param args:
        :param kwargs:
        :return:
        '''
        status = yield self.get_process_info(self.process_name)
        if status['state'] == 20:
            self.write(
                {
                    'status':'fail',
                    'reason':'stillrunning'
                }
            )
        else:
            yield self.direct_start_process(self.process_name)
            status = yield self.get_process_info(self.process_name)
            status['status'] = 'success'
            self.write(status)

    @gen.coroutine
    def delete(self, *args, **kwargs):
        '''
        强行停止爬虫
        :param args:
        :param kwargs:
        :return:
        '''
        status = yield self.get_process_info(self.process_name)
        if status['state']== 20:
            body = json.loads(self.request.body.decode('utf-8'))
            if body.get('sigint', True):
                yield self.stop_process(self.process_name)
                self.write({"status":"success"})
            else:
                yield self.force_stop_process(self.process_name)
                self.write({"status":"success"})
            pass
        else:
            status['status'] = 'faile'
            status['reason'] = 'Not running'
            self.write(status)

class XMLYTopnManager(XXXManager):

    r = redis.Redis(connection_pool=redis_pool)

    @run_on_executor
    def set_topn_n_and_topn_table(self,topn_n):
        self.r.set(ConfUtil.xmly_topn_n_key(),topn_n)
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        table_name =  'xmly_top%d_%s' % (topn_n, now)
        self.r.set(ConfUtil.xmly_topn_table_key(), table_name)

    @gen.coroutine
    def post(self, *args, **kwargs):
        status = yield self.get_process_info(self.process_name)
        print status
        if status.get('state',0) == 20:
            self.write({
                'status':'fail',
                'reason':"stillrunning"
            })
        else:
            body = json.loads(self.request.body.decode('utf-8'))
            topn_n = body.get('topn_n',None)
            if not topn_n:
                self.write({
                    'status':'fail',
                    'reason':"Body must contain topn_n parm"
                })
                return
            topn_n = int(topn_n)
            yield self.set_topn_n_and_topn_table(topn_n)
            yield self.direct_start_process(self.process_name)
            status = yield self.get_process_info(self.process_name)
            status['status'] = 'success'
            self.write(status)

class QtTopnManager(XXXManager):

    @gen.coroutine
    def post(self, *args, **kwargs):
        status = yield self.get_process_info(self.process_name)
        if status['state'] == 20:
            self.write({
                'status':"fail",
                "reason":"stillrunning"
            })
        else:
            body = json.loads(self.request.body.decode('utf-8'))
            if not body.get('topn_n',None):
                self.write({
                    "status":"fail",
                    "reason":"Body must contain topn_n parm"
                })
            else:
                yield self.direct_start_process(self.process_name)
                status = yield self.get_process_info(self.process_name)
                status['status'] = 'success'
                self.write(status)

