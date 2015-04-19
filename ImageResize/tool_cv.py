#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ---------Edit By KaiHangYang----------
# -------------2015,04,04---------------
import cv
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
    img = cv.LoadImage(path, 1)
    initH = img.height
    initW = img.width

    W = int(initW*m - m)
    H = int(initH*n - n)

    Img = cv.CreateImage((W, H), img.depth, img.nChannels)

    sum = [0, 0, 0]
    for i in xrange(W):
        for j in xrange(H):
            x = int(math.floor((j+1)/m-1))
            y = int(math.floor((i+1)/n-1))
            x = 0 if x <= 0 else x
            y = 0 if y <= 0 else y
            p = (j+0.0)/m - x
            q = (i+0.0)/n - y
            # 这里是传递4个像素数据以及p q
            for k in range(3):
                sum[k] = linear((int(img[x, y][k]),
                                 int(img[x+1, y][k]),
                                 int(img[x, y+1][k]),
                                 int(img[x+1, y+1][k])), p, q)

            Img[j, i] = tuple(sum)

    return Img


def resize_cubic(path, w, h):
    img = cv.LoadImage(path, 1)
    initW = img.width
    initH = img.height

    size = (W, H) = (int(initW*w-w), int(initH*h-h))
    sum = [0, 0, 0]

    Img = cv.CreateImage(size, img.depth, img.nChannels)

    for i in xrange(W):
        for j in xrange(H):
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
            p = -1.0 if p < -1.0 else p
            q = -1.0 if q < -1.0 else q
            for k in xrange(3):
                vals = ((int(img[y-1, x-1][k]), int(img[y, x-1][k]), int(img[y+1, x-1][k]), int(img[y+2, x-1][k])),
                        (int(img[y-1, x][k]), int(img[y, x][k]), int(img[y+1, x][k]), int(img[y+2, x][k])),
                        (int(img[y-1, x+1][k]), int(img[y, x+1][k]), int(img[y+1, x+1][k]), int(img[y+2, x+1][k])),
                        (int(img[y-1, x+2][k]), int(img[y, x+2][k]), int(img[y+1, x+2][k]), int(img[y+2, x+2][k])),
                        )
                sum[k] = cubic(vals, p, q)
                # 这里和cv2不同，溢出的话会为255

                if sum[k] >= 255: sum[k] = 255

            Img[j, i] = tuple(sum)
    return Img

if __name__ == '__main__':
    t1 = time.time()
    img = resize_cubic("haha.jpg", 1.5, 1.5)
    print time.time() - t1
    # cv.SaveImage("hehe_cv.jpg", img)
    cv.ShowImage('Test', img)
    cv.WaitKey(0)
