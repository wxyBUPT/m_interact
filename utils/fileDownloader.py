#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

from collections import defaultdict
import os
import os.path
import logging
import hashlib

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from utils.misc import md5sum

logger = logging.getLogger(__name__)

class FileException(Exception):
    """GEneral media error exception"""

class FSFilesStore(object):

    def __init__(self, basedir):
        if '://' in basedir:
            basedir = basedir.split('://',1)[1]
        self.basedir = basedir
        self._mkdir(self.basedir)
        self.created_directories = defaultdict(set())

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

    def __init__(self,store_uri):
        self.store = self._get_store(store_uri)

    def _get_store(self, store_uri):
        return FSFilesStore(store_uri)

    # 从url地址下载文件，并存储
    @gen.coroutine
    def download_file(self, url, basedir=None):
        print u'在这里下载文件'
        client = AsyncHTTPClient()
        response = yield client.fetch(url)

        if response.status != 200:
            logger.warning(
                'File (code: %(status)s): Error downloading file form '
                '%(url)s',
                {
                    'status':response.status,
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
            {"status":response.status,'url':url}
        )
        path = self.file_path(url)
        checksum = self.file_downloaded(response, url)
        raise gen.Return({'url':url,'path':path,'checksum':checksum})

    # 将下载
    def file_downloaded(self,response,url):
        path = self.file_path(url)
        buf = BytesIO(response.body)
        self.store.persist_file(path, buf)
        checksum = md5sum(buf)
        return checksum

        pass

    def file_path(self, url):
        media_guid = hashlib.sha1(url).hexdigest()
        media_ext = os.path.splitext(url)[1]
        return 'full/%s/%s' % (media_guid, media_ext)




def foo(url):
    print url
