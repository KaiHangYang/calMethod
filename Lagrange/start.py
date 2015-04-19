#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ---------Edit By KaiHangYang----------
# -------------2015,04,19---------------
from Tkinter import *
import numpy as np
import matplotlib
import tkMessageBox
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

class Application():

    # 对布局进行初始化
    def __init__(self):
        self.root = Tk()
        self.root.geometry("600x500")
        self.root.title("拉格朗日插值")

        self.view = Frame(self.root)
        self.view.pack(side=TOP, fill=X)

        self.control = Frame(self.root)
        self.control.pack(side=BOTTOM, fill=X)

        self.figure = Figure(figsize=(5,4), dpi=100)

        self.graph = self.figure.add_subplot(111)

        # self.graph.plot(x, y) x 和 y 是点集
        # self.graph.clear()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.view)
        self.canvas.show()

        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.view)

        self.nentry = Entry(self.control)
        self.nentry.grid(column=1, row=0)
        self.genbtn = Button(self.control)
        self.genbtn.grid(column=2, row=0)

        Label(self.control, text="n的值：").grid(row=0, column=0)

        Label(self.control, text="x的值：").grid(row=1, column=0)

        self.numbtn = Button(self.control)
        self.numbtn.grid(column=2, row=1)
        self.label = Label(self.control)
        self.label.grid(column=0, row=2, columnspan=3)

        self.xentry = Entry(self.control)
        self.xentry.grid(column=1, row=1)
        # 先生成基础函数图像
        self.baseX = list(np.arange(-5.0, 5.0, 0.02))
        self.baseX.append(5.0)
        self.baseX = np.array(self.baseX)

        self.baseY = map(lambda x: 1.0/(1+x*x), self.baseX)
        self.graph.plot(self.baseX, self.baseY)
        self.__config()
        self.root.mainloop()
    def __config(self):

        self.numn = StringVar()
        self.numn.set("10")
        self.nentry.config(textvariable=self.numn)

        self.genbtn.config(text="生成图像", command=self.drawGraph)
        self.numbtn.config(text="插值和误差", command=self.getX)
        self.numx = StringVar()
        self.numx.set("4.8")
        self.xentry.config(textvariable=self.numx)

        self.info = StringVar()
        self.info.set("显示结果")
        self.label.config(textvariable=self.info)

    def drawGraph(self):
        n = self.numn.get()
        if n.isdigit():
            # 先对原始图像进行清理
            self.graph.clear()
            # 重绘base图像
            self.graph.plot(self.baseX, self.baseY)

            n = int(n)

            print n

            self.xCollection = list(np.arange(-5.0, 5.0, 10.0/n))
            self.xCollection.append(5.0)
            self.xCollection = np.array(self.xCollection)

            self.yCollection = map(lambda x: 1.0/(1+x*x), self.xCollection)
            self.graph.scatter(self.xCollection, self.yCollection, color = "green")
            # 这一步是必须的
            self.canvas.show()
        else:
            tkMessageBox.showerror(title="Error", message="请输入整数n")
            return

    def getX(self):
        x = self.xentry.get()
        try:
            x = float(x)
        except:
            tkMessageBox.showerror(title="Error", message="x的数值有误, 请输出有理数。")
            return
        else:
            # 计算差值
            n = self.numn.get()

            if n.isdigit():
                n = int(n)
                h = 10.0/n
                xColl = list(np.arange(-5.0, 5.0, h))
                xColl.append(5.0)
                xColl = np.array(xColl)
                yColl = map(lambda x: 1.0/(1+x*x), xColl)

                y = 0
                for i in xrange(n+1):

                    l = 1.0
                    for j in xrange(n+1):
                        if j != i:
                            l *= (x-xColl[j])/(xColl[i]-xColl[j])

                    print l
                    y += l * yColl[i]

                self.info.set("插值结果是：(%0.2f, %0.2f)，误差是：%0.4f"%(x, y, (1.0/(1+x*x)-y)))
                # 把那个点画出来
                self.graph.scatter([x], [y], color="black")
                self.canvas.show()

            else:
                tkMessageBox.showerror(title="Error", message="请输入整数n")
                return

app = Application()
