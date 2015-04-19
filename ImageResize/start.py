#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ---------Edit By KaiHangYang----------
# -------------2015,04,12---------------
import os
import cv2
import sys
import time
from Tkinter import *
from PIL import (
    Image,
    ImageTk,
)
import tkFileDialog
import tkMessageBox
# 下来是我自己的辅助库
import fileCheck
import tool_cv2

# 解决Unicode Error
reload(sys)
sys.setdefaultencoding("utf8")
'''
    库引用说明：
        Tkinter 提供了GUI界面支持
        tkFileDialog提供了文件弹出窗口支持
        tkMessageBox提供了对话框支持
        PIL中的组件是提供图片打开支持的，用于在canvas上显示图片预览
'''

IMAGE_TYPES = [
    "jpg",
    "jpeg",
    "png",
    "tif",
    "bmp",
    "gif",
]

class Application():
    # 初始化
    def __init__(self):
        self.root = Tk()
        self.root.title("图片放大缩小的差值实现")
        self.root.resizable(width=True, height=True)
        self.root.maxsize(700, 600)
        self.root.minsize(670, 590)
        def hehe(a):
            print a
        self._inited = False
        # 声明上层部件框
        self.menu = Menu(self.root)
        self.viewpanel = Frame(self.root)
        self.managepanel = Frame(self.root)
        # 视窗部件的初始化
        self.filename = ''
        self.__menu()
        self.__scrollbar()
        self.__view()
        self.__manage()
        self.__bind_all()

        self.consoleNor("程序加载完毕！")
        self._inited = True
    def __menu(self):
        # 主菜单
        if self._inited:
            return

        self.root.config(menu=self.menu)
        # 文件菜单
        filemenu = Menu(self.menu, name="file")
        info = Menu(self.menu)
        self.menu.add_cascade(label="程序", menu=filemenu)
        self.menu.add_cascade(label="关于", menu=info)
        filemenu.add_command(label="打开<C-o>", command=self._getFileName)
        filemenu.add_command(label="保存<C-s>", command=self._save)
        filemenu.add_command(label="预览<C-p>", command=self._preview)

        filemenu.add_separator()
        filemenu.add_command(label="退出<C-q>", command=self.root.quit)

        info.add_command(label="声明", command=self._info)

    def __scrollbar(self):
        if self._inited:
            return

        # 后期要加上滚动事件
        self.hbar = Scrollbar(self.viewpanel, orient=HORIZONTAL)
        self.vbar = Scrollbar(self.viewpanel)

        # 位置，距离
        self.hbar.set(0, 0.5)
        self.vbar.set(0, 0.5)

        self.hbar.pack(side=BOTTOM, fill=X)
        self.vbar.pack(side=RIGHT, fill=Y)


    def __view(self):
        if self._inited:
            return

        self.viewpanel.pack(side=TOP, fill=X)
        self.canvas = Canvas(self.viewpanel)
        self.canvas.pack(expand=True, fill=BOTH)

        self.canvas.config(width=600, height=400, scrollregion=(0, 0, 600, 400))

    def __manage(self):
        if self._inited:
            return

        # 注意每次向console插入完数据之后需要使用 console.yview(END)来滚动到底
        self.managepanel.pack(side=BOTTOM, fill=X, pady=10)

        self.consolepanel = Frame(self.managepanel)
        self.controlpanel = Frame(self.managepanel)

        self.consolepanel.pack(side=LEFT, fill=Y, padx=10)
        self.controlpanel.pack(side=RIGHT, fill=Y, padx=10)

        self.controlpanel.columnconfigure(0, minsize=70)
        self.controlpanel.columnconfigure(1, minsize=70)
        self.controlpanel.columnconfigure(2, minsize=70)
        self.controlpanel.columnconfigure(3, minsize=70)

        # 首先是console
        self.console = Text(self.consolepanel, width=45, height=8, bd=1,
                            highlightbackground="grey", highlightthickness=1,
                            highlightcolor="grey", takefocus=0)
        self.console.pack(expand=True, fill=BOTH, padx=5, pady=5)

        # 设置不同信息类型的样式
        self.console.tag_config("error", background="red", foreground="white")
        self.console.tag_config("warning", background="yellow", foreground="black")
        # 设置不能输入 takefocus设置是不能被focus到
        self.console.bind("<KeyPress>", lambda x: "break")
        self.console.bind("<Button>", lambda x: "break")
        # 然后是control
        # 设置控制框标签
        self.fileName = StringVar()
        self.fileName.set("请选择图片文件")

        fileLabel = Label(self.controlpanel, textvariable=self.fileName, pady=2,
                          width=18)

        algLabel = Label(self.controlpanel, text="选择算法：")
        sizeLabel = Label(self.controlpanel, text="放大倍数:")
        wLabel = Label(self.controlpanel, text="宽度", pady=2)
        hLabel = Label(self.controlpanel, text="高度", pady=2)
        # 设置控制控件
        self.fileBtn = Button(self.controlpanel, text="添加图片", pady=2)

        self.algNum = IntVar()
        algRadio = []
        algRadio.append(Radiobutton(self.controlpanel, variable=self.algNum,
                                    text="双线性", value=0, pady=2))
        algRadio.append(Radiobutton(self.controlpanel, variable=self.algNum,
                                    text="三次卷积", value=1, pady=2))

        # 大小的有效性验证
        def sizeValidate(content):
            if content == "." or content.isdigit():
                return True
            else:
                return False

        self.wVar = StringVar()
        self.hVar = StringVar()
        wSize = Entry(self.controlpanel, textvariable=self.wVar, validate="key",
                      validatecommand=(self.root.register(sizeValidate), "%S"),
                      width=7)
        self.focus_entry = wSize
        hSize = Entry(self.controlpanel, textvariable=self.hVar, validate="key",
                      validatecommand=(self.root.register(sizeValidate), "%S"),
                      width=7)

        self.preBtn = Button(self.controlpanel, text="预览", pady=3)
        self.genBtn = Button(self.controlpanel, text="保存",
                             command=lambda x: x, pady=3)
        # 规划布局
        fileLabel.grid(row=0, column=0, columnspan=2, sticky=W)
        self.fileBtn.grid(row=0, column=2, columnspan=2, sticky=W)

        algLabel.grid(row=1, column=0, sticky=W)
        algRadio[0].grid(row=2, column=0, columnspan=2)
        algRadio[1].grid(row=2, column=2, columnspan=2)

        sizeLabel.grid(row=3, column=0, sticky=W)
        wLabel.grid(row=4, column=0, sticky=E)
        wSize.grid(row=4, column=1, sticky=W)
        hLabel.grid(row=4, column=2, sticky=E)
        hSize.grid(row=4, column=3, sticky=W)

        self.preBtn.grid(row=5, column=0, columnspan=2)
        self.genBtn.grid(row=5, column=2, columnspan=2)


    def _getFileName(self, *arg):
        name = tkFileDialog.askopenfilename()
        if name == "": return
        if fileCheck.isImage(name)[0]:
            self.filename = name
            self.fileName.set("已选择")
            self.consoleNor("选择图片："+os.path.basename(name))
            self._preview(True)
            return True
        else:
            tkMessageBox.showerror(title="Error",
                                   message="类型错误："
                                   "打开的不是图片呦，是不是打开的方式不对？")
            self.consoleErr("类型错误："+name+
                            "不是图片的类型，或者无法识别类型。")
            return False

    def _preview(self, *arg):
        # 在显示图片的时候需要保存对于那个图片的引用，
        # 否则python会在这个函数结束的时候，image的所有引用都没了，
        # 图片就显示不出来了
        if not(len(arg) == 0) and arg[0] == True:
            self.wScale = 1
            self.hScale = 1
        else:
            self.wScale = self.wVar.get()
            self.hScale = self.hVar.get()

            if self.wScale == "" or self.hScale == "":
                self.consoleWar("倍数警告：倍数未填写默认为（1，1）。")
                self.wScale = 1
                self.hScale = 1
            else:
                try:
                    self.wScale = float(self.wScale)
                    self.hScale = float(self.hScale)
                except:
                    self.wScale = 1
                    self.hScale = 1
                    self.consoleErr("数值错误：放大倍数非数值类型！")
                    return False
                else:
                    self.consoleNor("缩放(%0.1f, %0.1f)倍。"%(self.wScale,
                                                                  self.hScale))

        name = self.filename
        # 需要检测一下文件的类型
        if not fileCheck.isImage(name)[0]:
            tkMessageBox.showerror(title="Error",
                                   message="类型错误："
                                   "打开的不是图片呦，是不是打开的方式不对？")
            self.consoleErr("类型错误："+name+
                            "不是图片的类型，或者无法识别类型。")
            return False

        self.canvas.delete(ALL)
        self.image = Image.open(name)
        width, height = self.image.size

        width *= self.wScale
        height *= self.hScale
        tmpIm = self.image.resize((int(width),int(height)))

        self.tkImage = ImageTk.PhotoImage(tmpIm)

        self.canvas.create_image(0, 0, image=self.tkImage, anchor="nw")
        self.canvas.config(scrollregion=(0, 0, width, height))
        self.consoleNor("预览图片："+os.path.basename(name))
        return True

    def consoleNor(self, message):
        existContent = self.console.get("0.0", END)
        if existContent.count("\n") >= 50:
            self.console.delete("0.0", "2.0")

        self.console.insert(END, message+"\n")
        self.console.yview(END)

    def consoleWar(self, message):
        self.consoleNor(message)
        # 获取最后的输入的字符串的位置并且对于那段文字加上警告样式
        info = self.console.get("0.0", END).strip()
        info = info.split("\n")
        infoLen = len(info)
        self.console.tag_add("warning", str(infoLen)+".0", str(infoLen+1)+".0")

    def consoleErr(self, message):
        self.consoleNor(message)
        # 获取最后的输入的字符串的位置并且对于那段文字加上警告样式
        info = self.console.get("0.0", END).strip()
        info = info.split("\n")
        infoLen = len(info)
        self.console.tag_add("error", str(infoLen)+".0", str(infoLen+1)+".0")

    def __bind_all(self):
        self.fileBtn.config(command=self._getFileName)
        self.preBtn.config(command=self._preview)
        self.genBtn.config(command=self._save)
        # canvas的移动
        self.hbar.config(command=self.canvas.xview)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=self.hbar.set,
                           yscrollcommand=self.vbar.set)
        # 强制转化focus位置
        # 快捷键绑定
        self.root.bind_all("<Control-s>", self._save)
        self.root.bind_all("<Control-o>", self._getFileName)
        self.root.bind_all("<Control-p>", self._preview)
        self.root.bind_all("<Control-q>", self._quit)

    def _save(self, *argv):
        if not self._preview(): return
        self.consoleNor("过程控制：图片正在处理中...")
        filepath = tkFileDialog.asksaveasfilename()

        filename = os.path.basename(filepath)
        dotNum = filename.count(".")

        if dotNum == 0:
            if filename == "" : return
            postfix = ".jpg"
        elif dotNum >= 2 or not (filename.split(".")[1] in IMAGE_TYPES):
            self.consoleErr("格式错误：文件名格式错误！")
            return
        else:
            postfix = ""

        if os.path.exists(self.filename) and fileCheck.isImage(self.filename):
            try:
                if self.algNum == 0:
                    im = tool_cv2.resize_linear(self.filename, self.wScale, self.hScale)
                else:
                    im = tool_cv2.resize_cubic(self.filename, self.wScale, self.hScale)
                self.consoleNor("过程控制：图片处理完毕，开始保存...")
                cv2.imwrite(filepath+postfix, im)
                self.consoleNor("过程控制：图片保存完毕...")
            except:
                self.consoleErr("过程控制：图片保存过程出现问题...")
        else:
            self.consoleErr("类型错误：打开的不是图片或者是文件不存在！")
    def _info(self):
        tkMessageBox.showinfo(title="声明", message="作者：杨凯航\ngithub：https://github.com/KaiHangYang/calMethod/tree/master/Lagrange")
    def _quit(self, *argv):
        self.root.quit()
if __name__ == "__main__":
    app = Application()
    app.root.mainloop()
    def a(event):
        print "asd"
    app.console.bind("<Control-s>", a)
