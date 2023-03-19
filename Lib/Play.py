# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/19
# @ Time 19:28
from threading import Event, Thread
from time import sleep

from win32api import keybd_event, MapVirtualKey
from win32con import KEYEVENTF_KEYUP

from Lib.MusicScore import MusicScore
from Lib.Util import Util


class Play:
    """
    弹琴逻辑
    """
    key_map = {
        "0": 49, "1": 50, "2": 51, "3": 52, "4": 53, "5": 54, "6": 55, "7": 56, "8": 57, "9": 58,
        "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
        "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
        "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90
    }

    def __init__(self):
        self.t = None

    def start(self, data, lyre):
        """
        开始弹琴
        调用此方法自动创建守护进程进行演奏
        :param data:琴谱数据
        :param lyre: 1.风物；2.老旧
        """
        data.replace(" ", "L")
        self.t = MyThread()
        self.t.setDaemon(True)
        if self.t.ready:
            try:
                self.t.lyre = lyre
                data_tmp = data.split("\n")
                self.t.arr.clear()
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
            self.t.start()
            self.t.ready = False
            self.t.state = True

    def suspend_continue(self):
        """
        暂停按钮触发
        """
        if not self.t.ready:
            if self.t.state:
                print("暂停")
                self.t.pause()
                self.t.state = False
            else:
                print("继续")
                self.t.resume()
                self.t.state = True

    def finish(self):
        """
        结束按钮触发
        """
        if not self.t.ready:
            self.t.kile()
            self.t = None

    @staticmethod
    def key_down(key):
        """
        按下按键
        :param key:按键值
        """
        key = key.upper()
        vk_code = Play.key_map[key]
        keybd_event(vk_code, MapVirtualKey(vk_code, 0), 0, 0)

    @staticmethod
    def key_up(key):
        """
        抬起按键
        :param key: 按键值
        """
        key = key.upper()
        vk_code = Play.key_map[key]
        keybd_event(vk_code, MapVirtualKey(vk_code, 0), KEYEVENTF_KEYUP, 0)

    @staticmethod
    def key_press(key):
        """
        点击按键（按下并抬起）
        :param key: 按键值
        """
        if key in ["L", "l"]:
            sleep(0.01)
            return
        Play.key_down(key)
        sleep(0.01)
        Play.key_up(key)

    @staticmethod
    def play_note(t, note, time_div, time_div_div, time_interval):
        """
        播放连接的音符
        :param t: 线程
        :param note: 相连的音符（中间无空格） 字符串类型
        :param time_div: 音符时值一次分割
        :param time_div_div: 音符时值二次分割
        :param time_interval: 单个小节的时值
        """
        play_time = time_interval / time_div / time_div_div
        j = 0
        while j < len(note):
            t.flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            if note[j] == '(':
                while 1:
                    j += 1
                    if note[j] == ')':
                        sleep(play_time)
                        j += 1
                        break
                    else:
                        Play.key_press(note[j])
            elif note[j].isalpha():
                Play.key_press(note[j])
                sleep(play_time)
                j += 1
            elif note[j] == '1':
                sleep(play_time)
                j += 1
            else:
                j += 1

    @staticmethod
    def count_note(note):
        """
        为连接的音符数计数
        :param note: 相连的音符（中间无空格） 字符串类型
        """
        j = 0
        count = 0
        while j < len(note):
            if note[j] == '(':
                count += 1
                while 1:
                    j += 1
                    if note[j] == ')':
                        j += 1
                        break
            else:
                count += 1
                j += 1
        return count

    @staticmethod
    def play_music(t, music, time_interval):
        """
        播放曲谱
        :param t: 线程
        :param music: 曲谱 字符串类型
        :param time_interval: 单个小节的时值
        """
        music_section = music.split("/")
        for j in range(len(music_section)):
            if music_section[j][-2:] == " ":
                music_section[j] += '1'
        for x in music_section:
            Notes = x.split()
            time_div = len(Notes)
            for y in Notes:
                time_div_div = Play.count_note(y)
                Play.play_note(t, y, time_div, time_div_div, time_interval)

    @staticmethod
    def play(t, data_play, lyre):
        """
        弹琴
        :param t: 线程
        :param data_play: 琴键
        :param lyre: 1.风物；2.老旧
        """
        tt = float(data_play.split("\n")[0])
        if lyre == 2:
            print("老旧")
            data_play = MusicScore.fwToLj(data_play)
        while True:
            Play.play_music(t, data_play[data_play.find("\n") + 1:].replace("\n", ""), tt)
            break


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
        self.ready = True
        self.state = False

    def init(self, arr, lyre):
        self.arr = arr
        self.lyre = lyre

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
                Play.play(self, i, self.lyre)
            print("演奏完成")
        except Exception:
            if not self.ready:
                self.ready = True
                self.kile()
