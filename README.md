# nowatermark

[![PyPI Version](https://img.shields.io/pypi/v/nowatermark.svg)](https://pypi.python.org/pypi/nowatermark)
[![Build Status](https://img.shields.io/travis/SixQuant/nowatermark/master.svg)](https://travis-ci.org/SixQuant/nowatermark)
[![Wheel Status](https://img.shields.io/badge/wheel-yes-brightgreen.svg)](https://pypi.python.org/pypi/nowatermark)
[![Coverage report](https://img.shields.io/codecov/c/github/SixQuant/nowatermark/master.svg)](https://codecov.io/github/SixQuant/nowatermark?branch=master)
[![Powered by SixQuant](https://img.shields.io/badge/powered%20by-SixQuant-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://sixquant.cn)

## Overview
remove watermark. 
根据水印模板图片自动寻找并去除图片中对应的水印，利用 Python 和 OpenCV 快速实现。


## Install

### Mac OS Install OpenCV for Python3

- with-python3用来告诉homebrew用来让opencv支持python3，
- C++11 用来告诉homebrew提供c++11支持，
- with-contrib 用来安装opencv的contrib支持。

```bash
$ brew install opencv3 --without-python --with-python3 --c++11 --with-contrib  
```

Verifying the installation：

```python
import cv2
print(cv2.__version__)
```

If you got this error: "ImportError: No module named 'cv2'", then your symlink might be corrupted, you need to link your opencv to python site-packages:
```bash
$ brew link --force opencv3
```

### Install nowatermark
```bash
$ pip3 install nowatermark
```

## Usage

```python
from nowatermark import WatermarkRemover

path = './data/'

watermark_template_filename = path + 'anjuke-watermark-template.jpg'
remover = WatermarkRemover()
remover.load_watermark_template(watermark_template_filename)

remover.remove_watermark(path + 'anjuke3.jpg', path + 'anjuke3-result.jpg')
remover.remove_watermark(path + 'anjuke4.jpg', path + 'anjuke4-result.jpg')

```

---

### Original
![Original](https://github.com/SixQuant/nowatermark/blob/master/data/anjuke2.jpg)

### Removed watermark
![Removed watermark](https://github.com/SixQuant/nowatermark/blob/master/data/anjuke2-result.jpg)

---

## Procedure

### Feature Matching(特征匹配)
* 对水印模板图片进行了一些初始化处理，比如二值化后去除非文字部分等
* 尝试了 OpenCV 的多种算法
  - 比如 ORB + Brute-Force，即蛮力匹配，对应 cv2.BFMatcher() 方法
  - 比如 SIFT + FLANN，即快速最近邻匹配，对应 cv2.BFMatcher() 方法
  - 比如 Template Matching，即模板匹配，对应 cv2.matchTemplate() 方法
* 最后发现 Template Matching 最简单方便，效果也最好。 
* 如果水印位置固定的话则可以跳过Feature Matching(特征匹配)，直接进行下一步的Inpainting(图片修复)

### Inpainting(图片修复)
* 修复图片前需要做一些前置处理
  - 首先要得到图片的去水印 Mask 图片，即和待处理图片一样大小的除了水印部分的文字部分外其他部分全部是黑色的位图
  - 因为前面对水印做了二值化等处理，最终效果发现会有水印轮廓，所以需要对 Mask 图片做一次膨胀处理覆盖掉轮廓
* 选用了Telea在2004年提出的Telea算法，即基于快速行进（FMM）的修复算法
  - 对应 cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)
  - 对应论文：[An Image Inpainting Technique Based on the Fast Marching Method (2004)](http://www.cs.rug.nl/~alext/PAPERS/JGT04/paper.pdf)

## Todo

* 由于某些图片的水印和背景图片相似程度太高，如何提高水印位置的识别正确率
* 改进修复图片算法，可以考虑用深度学习来做做看？
* Google CVPR 2017, [《On the Effectiveness of Visible Watermarks》](https://watermark-cvpr17.github.io)这个据说很牛的，回头可以读一读

## License

[MIT](https://tldrlegal.com/license/mit-license)
