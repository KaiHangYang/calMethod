基于插值法的图像处理
===

思考与进度
---
+ 使用了双线性插值方法，和三次卷积公式
+ 动态库的编译方法是 
`gcc -fpic -c -l/usr/include/python2.7 -l /usr/lib/python2.7/config getVal.c`
`gcc -shared -o getVal.so getVal.o`
+ 在mac上面可能会有点不同

+ mac上面的动态库编译方法是`gcc -dynamiclib -I /System/Library/Frameworks/Python.framework/Versions/2.7/Headers/ -lpython2.7 -o getVal.dylib getVal.c;mv getVal.dylib getVal.so` *上面的路径是通过python中的sys.path找到的（*
+ 在window下面还蛋疼一些详细请见[window下Python使用C编写扩展库](http://en.wikibooks.org/wiki/Python_Programming/Extending_with_C)但是其中不能编译成**dll**文件要编译成**pyd**才能在Python中识别，并且扩展写的方式也不太一样（就是那个初始化函数的声明不太一样）具体编译方法类似`cl /LD hellomodule.c /Ic:\Python24\include c:\Python24\libs\python24.lib /link/out:hello.pyd`
+ 使用了cv2代替了之前的cv，而且使用numpy中的item来获取像素数据，效率要比cv的效率还要高。
+ 一下是我使用的时候的[心得和坑](https://www.evernote.com/shard/s452/sh/b10ee96f-d914-4f9b-8035-06553922632b/4a430634a67e8f014712d8241a702899)

未完成的事项
---
+ 还没有做通道检测，不过应该很简单了
+ 还没有进行window下的打包，没什么难度了
