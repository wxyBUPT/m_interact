#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

import unittest


class TestFoo(unittest.TestCase):

    def testFoo(self):
        print u'我在这里被调用了'
        self.assertIsNotNone("wang")

