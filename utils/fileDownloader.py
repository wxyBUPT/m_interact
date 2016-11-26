#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

from collections import defaultdict
import os
import os.path
import logging
import hashlib
import datetime
from datetime import timedelta


try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
import redis

from utils.misc import md5sum

logger = logging.getLogger(__name__)

from resourceses.resourceses import redis_pool

class FileException(Exception):
    """GEneral media error exception"""

class FSFilesStore(object):

    def __init__(self, basedir):
        if '://' in basedir:
            basedir = basedir.split('://',1)[1]
        self.basedir = basedir
        self._mkdir(self.basedir)

    def persist_file(self, path, buf):
        absolute_path = self._get_filesystem_path(path)
        self._mkdir(os.path.dirname(absolute_path))
        with open(absolute_path, 'wb') as f:
            f.write(buf.getvalue())

    def stat_file(self, path):
        absolute_path = self._get_filesystem_path(path)
        try:
            last_modified = os.path.getmtime(absolute_path)
        except: # FIXME: catching everything!
            return {}

        with open(absolute_path,'rb') as f:
            checksum = md5sum(f)
        return {'last_modified': last_modified, 'checksum': checksum}

    def _mkdir(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def _get_filesystem_path(self, path):
        path_comps = path.split('/')
        return os.path.join(self.basedir, *path_comps)

class FilesDownloader(object):

    redis = redis.Redis(connection_pool=redis_pool)

    def __init__(self,store_uri):
        self.store = self._get_store(store_uri)
        self.base = store_uri

    def _get_store(self, store_uri):
        return FSFilesStore(store_uri)

    # 从url地址下载文件，并存储
    @gen.coroutine
    def download_file(self, url):
        if not url:
            raise gen.Return(None)
        # 避免重复下载,如果缓存中有则直接返回
        cache = self.redis.hgetall(url)
        if cache:
            # 重新设置缓存时间
            logger.debug(
                'File meta in redis, path is %(path)s',
                {"path":cache.get('path',None)}
            )
            self.redis.expire(url,timedelta(1))
            raise gen.Return(cache)
        client = AsyncHTTPClient()
        response = yield client.fetch(url)

        if response.code!= 200:
            logger.warning(
                'File (code: %(status)s): Error downloading file form '
                '%(url)s',
                {
                    'status':response.code,
                    'url':url
                }
            )
            raise FileException('download-erro')

        if not response.body:
            logger.warning(
                'File (empty-content): Emptyy file from %(url)s',
                {'url':url}
            )
            raise FileException('empty-content')
        logger.debug(
            'File (%(status)s): Downloaded file from %(url)s' ,
            {"status":response.code,'url':url}
        )
        path = self.file_path(url)
        checksum = self.file_downloaded(response, url)
        res = {'url':url,'path':self.base + '/' + path,'checksum':checksum}
        logger.debug(
            'Cache file meta in redis, path is %(path)s',
            {"path":res.get('path',None)}
        )
        self.redis.hmset(url,res)
        self.redis.expire(url, timedelta(days=1))
        raise gen.Return(res)

    # 将下载
    def file_downloaded(self,response,url):
        path = self.file_path(url)
        buf = BytesIO(response.body)
        self.store.persist_file(path, buf)
        checksum = md5sum(buf)
        return checksum

    def file_path(self, url):
        media_guid = hashlib.sha1(url).hexdigest()
        media_ext = os.path.splitext(url)[1]
        now = datetime.datetime.now()
        return '%s/%d/%d/%d/%s%s' % (
            media_ext[1:],
            now.year,
            now.month,
            now.day,
            media_guid,
            media_ext)