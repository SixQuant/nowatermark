# coding=utf-8

import os
import sys
import unittest

root = os.path.abspath(os.path.expanduser(__file__ + '/../..'))
sys.path.append(root)

import nowatermark


class TestMethods(unittest.TestCase):
    def test_all(self):
        remover = nowatermark.WatermarkRemover()

        path = root + '/data/'
        watermark_template_filename = path + 'anjuke-watermark-template.jpg'
        remover.load_watermark_template(watermark_template_filename)

        self.assertIsNotNone(remover.remove_watermark(path + 'anjuke2.jpg', path + 'anjuke2-result.jpg'))


if __name__ == '__main__':
    unittest.main()
