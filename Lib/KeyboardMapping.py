# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/19
# @ Time 22:34
from ctypes import c_long, pythonapi, py_object
from inspect import isclass
from os import system
from threading import Thread


class KeyboardMapping:
    """
    键盘映射类
    """

    def __init__(self):
        self.t = None

    @staticmethod
    def stop_thread(thread):
        """
        杀死进程
        :param thread: 进程
        """
        tid = thread.ident
        exc = SystemExit
        """raises the exception, performs cleanup if needed"""
        tid = c_long(tid)
        if not isclass(exc):
            exc = type(exc)
        res = pythonapi.PyThreadState_SetAsyncExc(tid, py_object(exc))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def start(self, fileName):
        """
        开启键盘映射
        :param fileName: 映射文件名称
        """
        system('chcp 65001')  # 修改输出编码方式
        self.t = MyThread()
        self.t.setDaemon(True)
        self.t.fileName = fileName
        self.t.start()

    def stop(self):
        """
        关闭键盘映射
        :return:
        """
        self.t.kile()
        self.t = None
        system("TASKKILL /IM KeyboardMapping.exe /F")


class MyThread(Thread):
    """
    开启键盘映射进程
    """

    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self.fileName = ""

    def kile(self):
        try:
            KeyboardMapping.stop_thread(self)
        except Exception:
            pass

    def run(self):
        system("..\\bin\\KeyboardMapping.exe ..\\keyMap\\%s.ahk &" % self.fileName)
