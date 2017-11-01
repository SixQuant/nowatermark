# coding=utf-8

import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.expanduser(__file__ + '/../..')))

import nowatermark


class TestMethods(unittest.TestCase):
    def test_add(self):
        remover = nowatermark.WatermarkRemover()
        self.assertIsNotNone(remover)


if __name__ == '__main__':
    unittest.main()
