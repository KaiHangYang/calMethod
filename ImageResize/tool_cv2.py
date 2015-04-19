#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ---------Edit By KaiHangYang----------
# -------------2015,04,04---------------
#import cv
import cv2
import numpy as np
import math
from getVal import (
    linear,
    cubic,
)
import time

# 目前两个版本只是针对于RGB三通道图片进行的处理扩展起来还是很容易的
# 对于1 ～ 3倍之内的图片放大和缩小建议使用双线性内差值法
# 效果和三次卷积法差不多而且速度会快上好多
#
# 对于其他的倍数放缩建议使用三次卷积内差值这样对于图片的处理效果会更加的好
# 首先边界不会过于模糊而且噪点也不会太多


def resize_linear(path, m, n):
    # img = cv.LoadImage(path, 1)
    img = cv2.imread(path)
    #initH = img.height
    initW, initH, nChannels = img.shape

    W = int(initW*m - m)
    H = int(initH*n - n)

    #Img = cv.CreateImage((W, H), img.depth, img.nChannels)
    Img = [[]]

    sum = [0, 0, 0]
    for i in xrange(W):

        x = (i+0.0)/m
        p = x - int(x)
        x = int(x)

        for j in xrange(H):

            y = (j+0.0)/n
            q = y - int(y)
            y = int(y)
            # 这里是传递4个像素数据以及p q
            for k in range(3):
                sum[k] = linear((img.item(x, y, k),
                                 img.item(x+1, y, k),
                                 img.item(x, y+1, k),
                                 img.item(x+1, y+1, k)), p, q)

                if sum[k] >= 255: sum[k] = 255

            Img[i].append(tuple(sum))
        Img.append([])
    Img.pop()
    return np.array(Img, np.uint8)


def resize_cubic(path, w, h):
    img = cv2.imread(path)

    initH, initW, nChannel = img.shape

    (W, H) = (int(initW*w-w), int(initH*h-h))
    sum = [0, 0, 0]
    Img = [[]]
    for j in xrange(H):
        for i in xrange(W):

            x = (i+0.0)/w
            y = (j+0.0)/h

            p = x - int(x)
            q = y - int(y)

            x = 1 if x <= 0 else (initW-3 if (x+2) >= initW else x)
            y = 1 if y <= 0 else (initH-3 if (y+2) >= initH else y)
            x = int(x)
            y = int(y)
            # 由于三次卷积的计算方式 如果使p q 小于-1的话会使像素的值大多数是0
            # 因此这里得进行判断将 p q的值控制在一定范围内
            p = -0.1 if p < -1.0 else p
            q = -0.1 if q < -1.0 else q
            for k in xrange(3):
                vals = ((img.item(y-1, x-1, k), img.item(y, x-1, k), img.item(y+1, x-1, k), img.item(y+2, x-1, k)),
                        (img.item(y-1, x, k), img.item(y, x, k), img.item(y+1, x, k), img.item(y+2, x, k)),
                        (img.item(y-1, x+1, k), img.item(y, x+1, k), img.item(y+1, x+1, k), img.item(y+2, x+1, k)),
                        (img.item(y-1, x+2, k), img.item(y, x+2, k), img.item(y+1, x+2, k), img.item(y+2, x+2, k)))
                sum[k] = cubic(vals, p, q)
                # 注意cv2因为是基于numpy
                # uint8的，所以如果超出255就会默认出现溢出，也就是会使数变得很
                # 同样小与零的数也是会出现这种情况的
                if sum[k] >= 255: sum[k] = 255
                if sum[k] <= 0: sum[k] = 0

            Img[j].append(tuple(sum))

        Img.append([])

    Img.pop()
    return np.array(Img, np.uint8)

if __name__ == '__main__':
    t1 = time.time()
    img = resize_cubic("haha.jpg", 1.5, 1.5)
    print time.time() - t1
    # cv2.imwrite("hehe_cv2.jpg", img)
    cv2.imshow('Test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
