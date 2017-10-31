# coding=utf-8

import cv2
import numpy as np

# 膨胀算法 Kernel
_DILATE_KERNEL = np.array([[0, 0, 1, 0, 0],
                           [0, 0, 1, 0, 0],
                           [1, 1, 1, 1, 1],
                           [0, 0, 1, 0, 0],
                           [0, 0, 1, 0, 0]], dtype=np.uint8)


class WatermarkRemover(object):
    """"
    去除图片中的水印(Remove Watermark)
    """

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.watermark_template_gray_img = None
        self.watermark_template_mask_img = None
        self.watermark_template_h = 0
        self.watermark_template_w = 0

    def load_watermark_template(self, watermark_template_filename):
        """
        加载水印模板，以便后面批量处理去除水印
        :param watermark_template_filename:
        :return:
        """
        self.generate_template_gray_and_mask(watermark_template_filename)

    def dilate(self, img):
        """
        对图片进行膨胀计算
        :param img:
        :return:
        """
        dilated = cv2.dilate(img, _DILATE_KERNEL)
        return dilated

    def generate_template_gray_and_mask(self, watermark_template_filename):
        """
        处理水印模板，生成对应的检索位图和掩码位图
        检索位图
            即处理后的灰度图，去除了非文字部分

        :param watermark_template_filename: 水印模板图片文件名称
        :return: x1, y1, x2, y2
        """

        # 水印模板原图
        img = cv2.imread(watermark_template_filename)

        # 灰度图、掩码图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

        mask = self.dilate(mask)  # 使得掩码膨胀一圈，以免留下边缘没有被修复
        #mask = self.dilate(mask)  # 使得掩码膨胀一圈，以免留下边缘没有被修复

        # 水印模板原图去除非文字部分
        img = cv2.bitwise_and(img, img, mask=mask)

        # 后面修图时需要用到三个通道
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        self.watermark_template_gray_img = gray
        self.watermark_template_mask_img = mask

        self.watermark_template_h = img.shape[0]
        self.watermark_template_w = img.shape[1]

        # cv2.imwrite('watermark-template-gray.jpg', gray)
        # cv2.imwrite('watermark-template-mask.jpg', mask)

        return gray, mask

    def find_watermark(self, filename):
        """
        从原图中寻找水印位置
        :param filename:
        :return: x1, y1, x2, y2
        """
        # Load the images in gray scale
        gray_img = cv2.imread(filename, 0)
        return self.find_watermark_from_gray(gray_img, self.watermark_template_gray_img)

    def find_watermark_from_gray(self, gray_img, watermark_template_gray_img):
        """
        从原图的灰度图中寻找水印位置
        :param gray_img: 原图的灰度图
        :param watermark_template_gray_img: 水印模板的灰度图
        :return: x1, y1, x2, y2
        """
        # Load the images in gray scale

        method = cv2.TM_CCOEFF
        # Apply template Matching
        res = cv2.matchTemplate(gray_img, watermark_template_gray_img, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            x, y = min_loc
        else:
            x, y = max_loc

        return x, y, x + self.watermark_template_w, y + self.watermark_template_h

    def remove_watermark_raw(self, img, watermark_template_gray_img, watermark_template_mask_img):
        """
        去除图片中的水印
        :param img: 待去除水印图片位图
        :param watermark_template_gray_img: 水印模板的灰度图片位图，用于确定水印位置
        :param watermark_template_mask_img: 水印模板的掩码图片位图，用于修复原始图片
        :return: 去除水印后的图片位图
        """
        # 寻找水印位置
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        x1, y1, x2, y2 = self.find_watermark_from_gray(img_gray, watermark_template_gray_img)

        # 制作原图的水印位置遮板
        mask = np.zeros(img.shape, np.uint8)
        # watermark_template_mask_img = cv2.cvtColor(watermark_template_gray_img, cv2.COLOR_GRAY2BGR)
        # mask[y1:y1 + self.watermark_template_h, x1:x1 + self.watermark_template_w] = watermark_template_mask_img
        mask[y1:y2, x1:x2] = watermark_template_mask_img
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        # 用遮板进行图片修复，使用 TELEA 算法
        dst = cv2.inpaint(img, mask, 4, cv2.INPAINT_TELEA)
        # cv2.imwrite('dst.jpg', dst)

        return dst

    def remove_watermark(self, filename, output_filename=None):
        """
        去除图片中的水印
        :param filename: 待去除水印图片文件名称
        :param output_filename: 去除水印图片后的输出文件名称
        :return: 去除水印后的图片位图
        """

        # 读取原图
        img = cv2.imread(filename)

        dst = self.remove_watermark_raw(img,
                                        self.watermark_template_gray_img,
                                        self.watermark_template_mask_img
                                        )

        if output_filename is not None:
            cv2.imwrite(output_filename, dst)

        return dst
