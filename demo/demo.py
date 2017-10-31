# coding=utf-8

from nowatermark import WatermarkRemover

path = '../data/'

watermark_template_filename = path + 'anjuke-watermark-template.jpg'
remover = WatermarkRemover()
remover.load_watermark_template(watermark_template_filename)

remover.remove_watermark(path + 'anjuke2.jpg', path + 'anjuke2-result.jpg')
remover.remove_watermark(path + 'anjuke3.jpg', path + 'anjuke3-result.jpg')
remover.remove_watermark(path + 'anjuke4.jpg', path + 'anjuke4-result.jpg')
