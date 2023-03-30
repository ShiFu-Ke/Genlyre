# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/18
# @ Time 22:24
from inspect import isclass
from ctypes import pythonapi, c_long, py_object
from os import path, system


class Util:
    """
    工具类
    """

    @staticmethod
    def init():
        """
        软件启动时调用
        """
        # 判断是否存在默认键盘映射文件，不存在就创建
        testMap = """Numpad1::A
Numpad2::S
Numpad3::D
Numpad4::F
Numpad5::G
Numpad6::H
Numpad7::J
Numpad8::Q
Numpad9::W
NumpadAdd::E
NumLock::R
NumpadDiv::T
NumpadMult::Y
NumpadSub::U"""
        if not path.exists("..\\keyMap\\default.ahk"):
            file = open("..\\keyMap\\default.ahk", 'w', encoding="UTF-8")
            file.write(testMap)
            file.close()

    @staticmethod
    def stop():
        """
        软件关闭是调用
        """
        # 再次关闭映射插件，防止中途异常没有正确关闭
        system("TASKKILL /IM KeyboardMapping.exe /F")

    @staticmethod
    def lcm(a, b):
        """
        求两个数的最小公倍数
        :param a: 数字1
        :param b: 数字2
        :return: 最小公倍数
        """
        for i in range(min(a, b), 0, -1):
            if a % i == 0 and b % i == 0:
                return a * b // i

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
