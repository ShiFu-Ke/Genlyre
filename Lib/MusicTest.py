# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/19
# @ Time 19:28
from threading import Event, Thread
from time import sleep

from playsound import playsound

from Lib.MusicScore import MusicScore
from util.Util import Util


class MusicTest:
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

    def start(self, data, lyre, pAdd):
        """
        开始弹琴
        调用此方法自动创建守护进程进行演奏
        :param data: 琴谱
        :param lyre: 音源 1：风物；2：老旧；3：镜花
        :param pAdd: 琶音提速
        """
        if self.t is None or self.t.ready:
            self.state = False
        if self.state:
            return
        self.state = True
        data.replace(" ", "L")
        self.t = MyThread()
        self.t.setDaemon(True)
        try:
            self.t.lyre = lyre
            self.t.pADD = pAdd
            data_tmp = data.split("\n")
            self.t.arr.clear()
            tmp = -1
            for i in data_tmp:
                try:
                    if "." in i:
                        float(i)
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

    @staticmethod
    def playMusic(t, data, lyre, pAdd=0):
        """
        开始演奏
        :param t:线程
        :param lyre: 音源
        :param data: 琴谱
        :param pAdd: 琶音提速，默认值为0
        """
        if "L" in data:
            data = data.replace("L", " ")
        time = float(data[:data.find("\n")])
        data_tmp = data.upper().replace("\n", "")
        data_end = ""
        for i in data_tmp:
            if i in ["/", "(", ")", "[", "]", " "] or i in MusicTest.keys:
                data_end += i
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
        arr_tmp = data_tmp.split("/")
        print(arr_tmp)
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
                    if i[j] in MusicTest.keys or i[j] == " ":
                        arr_tmp.append(i[j])
                    elif i[j] == "(":
                        tmp_bracket = True
            length_max = Util.lcm(length_max, len(arr_tmp))
            arr_data.append(arr_tmp.copy())
        arr.clear()
        # 开始演奏
        for i in arr_data:
            length = len(i)
            time_tmp = time / length
            for j in i:
                for k in j:
                    if k in MusicTest.keys:
                        if lyre == 1:
                            Thread(daemon=True,
                                   target=lambda: MusicTest.playAKey("app/resource/sound/FengWu/" + k + ".wav")).start()
                        elif lyre == 2:
                            Thread(daemon=True,
                                   target=lambda: MusicTest.playAKey("app/resource/sound/LaoJiu/" + k + ".wav")).start()
                        else:
                            Thread(daemon=True,
                                   target=lambda: MusicTest.playAKey("app/resource/sound/JingHua/" + k + ".wav")).start()
                sleep(time_tmp)
                t.flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回

    @staticmethod
    def playAKey(key):
        playsound(key)

    @staticmethod
    def isKe(data):
        """
        刻师傅琴谱格式测试
        :param data:琴谱
        :return: 格式正确返回True，否则返回False；提示信息
        """
        try:
            float(data[:data.find("\n")])
            data_tmp = data[:data.find("\n")]
            if "." not in data_tmp:
                return False, "首行必须是小数，整数请加\".0\"（如：1.0）！"
            tmp01 = 0
            for i in MusicScore.nuToJp(data[data.find("\n") + 1:]).upper():
                if i in MusicTest.keys:
                    tmp01 = 1
                    break
            if tmp01 == 0:
                return False, "琴谱内容为空！"
            tmp01 = 0
            tmp02 = 0
            hang = 1  # 行位置
            lie = 1  # 列位置
            try:
                for i in data:
                    lie += 1
                    if i == "\n":
                        hang += 1
                        lie = 0
                    if i == "(":
                        tmp01 += 1
                    elif i == ")":
                        tmp01 -= 1
                    elif i == "[":
                        tmp02 += 1
                    elif i == "]":
                        tmp02 -= 1
                    elif i == "/":
                        if tmp01 != 0 or tmp02 != 0:
                            return False, "第" + str(hang) + "行，第" + str(lie) + "列存在不匹配的括号！"
                    if tmp01 not in [0, 1] or tmp02 not in [0, 1]:
                        return False, "第" + str(hang) + "行，第" + str(lie) + "列存在不匹配的括号！"
            except IndexError:
                return False, "存在不匹配的括号！"
            if tmp01 != 0:
                return False, "第" + str(hang) + "行，第" + str(lie) + "列存在不匹配的括号！"
            return True, "文件格式正确！"
        except Exception as e:
            return False, "首行必须是数字(必须小数，如：1.0)！"


class MyThread(Thread):
    """
    弹琴进程
    """

    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self.flag = Event()  # 用于暂停线程的标识
        self.flag.set()  # 设置为True
        self.arr = []
        self.lyre = 1
        self.pADD = 0
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
            for i in self.arr:
                if len(i.split("\n")) <= 2:  # 防止没有音符导致卡死
                    i += "L"
                MusicTest.playMusic(self, i, self.lyre, self.pADD)
            self.ready = True
            print("演奏完成")
        except Exception:
            if not self.ready:
                self.ready = True
                self.kile()
