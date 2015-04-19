#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ---------Edit By KaiHangYang----------
# -------------2015,04,04---------------
# 获取bilinera interpolation
from PIL import Image
import math
from getVal import linear
import time


# 这个是使用二元函数线性插值做的
'''
    经过测试使用c的扩展仅仅是提高了1.3s的时间
    测试cv库的速度
'''


def resize(img, m, n):
    initW, initH = img.size

    W = int(initW*m - m)
    H = int(initH*n - n)

    Img = Image.new(img.mode, (W, H))

    sum = [0, 0, 0]
    for i in xrange(H):
        for j in xrange(W):
            x = int(math.floor((j+1)/m-1))
            y = int(math.floor((i+1)/n-1))
            x = 0 if x <= 0 else x
            y = 0 if y <= 0 else y
            p = (j+0.0)/m - x
            q = (i+0.0)/n - y

            # 这里是传递4个像素数据以及p q
            for k in range(3):
                sum[k] = linear((img.getpixel((x, y))[k],
                                 img.getpixel((x+1, y))[k],
                                 img.getpixel((x, y+1))[k],
                                 img.getpixel((x+1, y+1))[k]), p, q)
                '''
                sum[k] = int(img.getpixel((x, y))[k]*(1-p)*(1-q) +
                          img.getpixel((x+1, y))[k]*p*(1-q) +
                          img.getpixel((x, y+1))[k]*(1-p)*q +
                          img.getpixel((x+1, y+1))[k]*p*q)'''

            Img.putpixel((j, i), tuple(sum))

    return Img

if __name__ == "__main__":
    t1 = time.time()
    im = Image.open('haha.jpg')
    resize(im, 2, 2).show()
    print (time.time() - t1)
