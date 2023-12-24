# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/19
# @ Time 19:28
from threading import Event, Thread
from time import sleep

from win32api import keybd_event, MapVirtualKey
from win32con import KEYEVENTF_KEYUP

from Lib.MusicScore import MusicScore
from Lib.midi import Midi
from util.Util import Util


class PlayMusic:
    """
    弹琴逻辑
    """
    keys = ["Z", "X", "C", "V", "B", "N", "M", "A", "S", "D", "F", "G", "H", "J", "Q", "W", "E", "R", "T", "Y", "U"]
    key_map = {
        "0": 49, "1": 50, "2": 51, "3": 52, "4": 53, "5": 54, "6": 55, "7": 56, "8": 57, "9": 58,
        "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
        "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
        "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90
    }

    def __init__(self):
        self.t = None
        self.state = False

    def start(self, filePath, scoreType, lyre, pAdd):
        """
        开始弹琴
        调用此方法自动创建守护进程进行演奏
        :param filePath: 琴谱文件路径
        :param scoreType: 琴谱格式；1：刻师傅，2：呱呱，3：伊蕾娜
        :param lyre: 1.风物；2.老旧
        :param pAdd: 琶音提速
        """
        if self.t is None or self.t.ready:
            self.state = False
        if self.state:
            return
        self.state = True
        self.t = MyThread()
        self.t.setDaemon(True)
        self.t.fileType = filePath[-3:]
        self.t.lyre = lyre
        self.t.arr.clear()

        if self.t.fileType == "mid":
            self.t.arr.append(filePath)
        elif self.t.fileType == "txt":
            file = open(filePath, encoding='utf-8')
            data = file.read()
            file.close()
            if scoreType == 1:
                pass
            elif scoreType == 2:
                data = MusicScore.guaToke(data)
            elif scoreType == 3:
                data = MusicScore.guaToke(MusicScore.yiToGua(data))
            data.replace(" ", "L")
            try:
                self.t.pADD = pAdd
                data_tmp = data.split("\n")
                tmp = -1
                for i in data_tmp:
                    try:
                        if "." in i:
                            self.t.arr.append("")
                            tmp += 1
                    except IndexError:
                        pass
                    if i.replace(" ", "") != "":
                        self.t.arr[tmp] += i + "\n"
            except Exception:
                return
            for i in range(len(self.t.arr)):
                self.t.arr[i] = MusicScore.nuToJp(self.t.arr[i])

        # 开始调用演奏进程
        self.t.start()
        self.t.ready = False
        self.t.state = True

    def suspend_continue(self):
        """
        暂停按钮触发
        """
        try:
            if not self.t.ready:
                if self.t.state:
                    print("暂停")
                    self.t.pause()
                    self.t.state = False
                else:
                    print("继续")
                    self.t.resume()
                    self.t.state = True
        except Exception:
            pass

    def finish(self):
        """
        结束按钮触发
        """
        try:
            if not self.t.ready:
                self.t.kile()
                self.t = None
                self.state = False
        except Exception:
            pass
        PlayMusic.key_upAll()

    @staticmethod
    def key_down(key):
        """
        按下按键
        :param key:按键值
        """
        key = key.upper()
        vk_code = PlayMusic.key_map[key]
        keybd_event(vk_code, MapVirtualKey(vk_code, 0), 0, 0)

    @staticmethod
    def key_up(key):
        """
        抬起按键
        :param key: 按键值
        """
        key = key.upper()
        vk_code = PlayMusic.key_map[key]
        keybd_event(vk_code, MapVirtualKey(vk_code, 0), KEYEVENTF_KEYUP, 0)

    @staticmethod
    def key_upAll():
        for i in PlayMusic.keys:
            PlayMusic.key_up(i)

    @staticmethod
    def playMusic(t, data, lyre, pAdd=0):
        """
        开始演奏
        :param t:线程
        :param data: 琴谱
        :param lyre: 1.风物；2.老旧
        :param pAdd: 琶音提速，默认值为0
        """
        if "L" in data:
            data = data.replace("L", " ")
        time = float(data[:data.find("\n")])
        data_tmp = data.upper().replace("\n", "")
        data_end = ""
        for i in data_tmp:
            if i in ["/", "(", ")", "[", "]", " "] or i in PlayMusic.keys:
                data_end += i
        # 如果是老旧，转换谱
        if lyre == 2:
            print("老旧")
            data_end = MusicScore.fwToLj(data_end)
        # 找琶音长度
        p_num = 0
        p_data = data_end[data_end.find("["):]
        while p_data.find("[") > -1:
            p_tmpLen = p_data.find("]") - p_data.find("[") - 1
            if p_tmpLen > p_num:
                p_num = p_tmpLen
            p_data = p_data[p_data.find("]") + 1:]
        p_num += pAdd

        # 将每拍放入数组
        data_tmp = data_end
        arr_tmp = data_tmp.split("/")[:-1]  # split切割后，后面会增加一个空字符串用[:-1]只取前面的
        arr = []
        for i in arr_tmp:
            if len(i) > 0:
                arr.append(i)
            elif i == "":
                arr.append(" ")
        for i in range(len(arr)):
            if "[" in arr[i]:
                p_tmp = ""
                p_kh = False
                p_py = False
                p_numTmp = 0  # 记录琶音中音的个数
                for j in arr[i]:
                    if j == "(":
                        p_kh = True
                    elif j == ")":
                        p_kh = False
                    elif j == "[":
                        p_py = True
                        p_numTmp = 0
                    elif j == "]":
                        p_tmp += " " * (p_num - p_numTmp + 1)
                        p_py = False
                        continue
                    if p_py:  # 如果是琶音
                        if j not in ["[", "]"]:
                            p_tmp += j
                            p_numTmp += 1
                        continue
                    if j not in ["[", "]"]:
                        p_tmp += j
                    if not p_kh:
                        p_tmp += " " * p_num
                arr[i] = p_tmp
        arr_data = []
        p_tmpLen = ""
        tmp_bracket = False  # 记录是否在括号内
        length_max = 1  # 记录每拍最多音个数
        for i in arr:
            arr_tmp.clear()
            for j in range(len(i)):
                if tmp_bracket:
                    p_tmpLen += i[j]
                    if i[j + 1] == ")":
                        tmp_bracket = False
                        arr_tmp.append(p_tmpLen)
                        p_tmpLen = ""
                else:
                    if i[j] in PlayMusic.keys or i[j] == " ":
                        arr_tmp.append(i[j])
                    elif i[j] == "(":
                        tmp_bracket = True
            length_max = Util.lcm(length_max, len(arr_tmp))
            arr_data.append(arr_tmp.copy())
        arr.clear()
        print(arr_data)
        # 开始演奏
        for i in arr_data:
            length = len(i)
            time_tmp = time / length
            for j in i:
                for k in j:
                    if k in PlayMusic.keys:
                        PlayMusic.key_down(k)
                        PlayMusic.key_up(k)
                sleep(time_tmp)
                t.flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回

    @staticmethod
    def playMid(t, data, lyre, time):
        """
        开始演奏Mid
        :param t:线程
        :param data: 琴谱
        :param lyre: 1.风物；2.老旧
        :param time: 时间参数
        """
        # 如果是老旧，转换谱
        if lyre == 2:
            print("老旧")
            data = MusicScore.fwToLj(data)
        tmp = ""
        bef = False  # 上一个是否为=
        for i in data:
            if i == "=":
                sleep(time)
                bef = True
            else:
                # 全部抬起
                if bef:
                    for k in tmp:
                        PlayMusic.key_up(k)
                    tmp = ""
                PlayMusic.key_down(i)
                tmp += i
                bef = False
            t.flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
        # 演奏完毕抬起所有按键
        PlayMusic.key_upAll()


class MyThread(Thread):
    """
    弹琴进程
    """

    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self.flag = Event()  # 用于暂停线程的标识
        self.flag.set()  # 设置为True
        self.arr = []
        '''
        文件为txt时存放音符，文件为mid在数组第一个位置时存放文件路径
        '''
        self.lyre = 1
        self.pADD = 0
        self.fileType = "txt"
        self.midTime = 0.5
        self.ready = True
        self.state = False

    def init(self, arr, lyre, pADD):
        self.arr = arr
        self.lyre = lyre
        self.pADD = pADD

    def pause(self):
        self.flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.flag.set()  # 将线程从暂停状态恢复, 如果已经暂停的话
        self.flag.clear()  # 设置为False

    def stopped(self):
        return self.flag.is_set()

    def kile(self):
        if not self.state:
            self.resume()
        Util.stop_thread(self)
        sleep(0.5)
        print("演奏结束")

    def run(self):
        print("开始演奏")
        try:
            if self.fileType == "mid":
                print("是mid")
                # PlayMusic.playMid(self, self.arr[0], self.lyre, self.midTime)
            elif self.fileType == "txt":
                for i in self.arr:
                    if len(i.split("\n")) <= 2:  # 防止没有音符导致卡死
                        i += "L"
                    PlayMusic.playMusic(self, i, self.lyre, self.pADD)
            self.ready = True
            print("演奏完成")
        except Exception:
            if not self.ready:
                self.ready = True
                self.kile()
