#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

import hashlib

def md5sum(file):
    """
    计算文件的MD5校验和，而不是将文件全部读入到内存中

    from io import BytesIO
    md5sum(BytesIO(b'file content to hash'))
    :param file:
    :return:
    """

    m = hashlib.md5()
    while 1:
        d = file.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()
