# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/18
# @ Time 22:24
from inspect import isclass
from ctypes import pythonapi, c_long, py_object


class Util:
    """
    工具类
    """

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
