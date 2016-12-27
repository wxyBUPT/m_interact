#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

'''
import unittest
'''


'''
class TestFoo(unittest.TestCase):

    def testFoo(self):
        print u'我在这里被调用了'
        self.assertIsNotNone("wang")
'''

my_mount = '/var/crawler/cnr_shares'
def changePathStyle( filePath):
    if filePath.startswith(my_mount):
        filePath = filePath[len(my_mount):]
    paths = filePath.split('/')
    filePath = '\\'.join(paths)
    return filePath



print u'被调用了'
if __name__ == "__main__":
    print changePathStyle('/var/crawler/cnr_shares/m4a/2016/12/26/e19af8357.m4a')
