# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/18
# @ Time 22:24
from re import findall
import subprocess
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
        if not path.exists("../data/default.ahk"):
            file = open("../data/default.ahk", 'w', encoding="UTF-8")
            file.write(testMap)
            file.close()

    @staticmethod
    def getMaxArpeggioLen(beat):
        """
        获取一拍中所有琶音中音的个数最大值，括号内同时按的音视为一个音。
        :param beat: 一拍音符。
        :return: 最大长度；int类型。
        """
        return max(
            list(
                map(lambda arr: len(findall(r'[a-zA-Z](?![a-zA-Z]*\))|\(\w+\)', arr)), findall(r'\[.*?]', beat))))

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

    @staticmethod
    def cmd(text):
        # 执行的命令
        command = text
        # 创建子进程并执行命令，在后台运行
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 获取命令的输出信息，包括标准输出和错误输出
        output, errors = p.communicate()
        # 输出结果
        print(output.decode('gbk'))
