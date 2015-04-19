#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ---------Edit By KaiHangYang----------
# -------------2015,04,16---------------
import struct
import os
# 检测的方式是通过检测文件头来判断MEMI类型来进行的
types = {
    u"FFD8FF": "jpg",
    u"89504E47": "png",
    u"47494638": "gif",
    u"49492A00": "tif",
    u"424D": "bmp",
}

def _getHex(b_tuple):
    num = len(b_tuple)
    string = u""

    for i in xrange(num):
        if b_tuple[i] < 10:
            string += "0"

        string += (u"%x"%b_tuple[i])

    return string

def isImage(path):
    if not os.path.exists(path):
        return (False, "undefined")
    with open(path, "rb") as f:
        for i in types.keys():
            head_size = len(i)/2
            f.seek(0)
            b_string = f.read(head_size)
            b_tuple = struct.unpack_from(head_size*"B", b_string)
            hex_string = _getHex(b_tuple)

            if i == hex_string.upper():
                return (True, types[i])

    return (False, "unkonwn")

