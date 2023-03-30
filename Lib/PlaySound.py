# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/28
# @ Time 17:53
from threading import Thread
from keyboard import wait, hook
from playsound import playsound


class PlaySound:
    """
    原琴类，可以模拟原琴发声
    """
    keyList = {"Q", "W", "E", "R", "T", "Y", "U", "A", "S", "D", "F", "G", "H", "J", "Z", "X", "C", "V", "B", "N", "M"}

    def __init__(self):
        t = Thread(target=self.on_key_event)
        t.daemon = True
        t.start()
        self.state = True
        self.lyre = 1

    def on_key_event(self):
        """
        启动键盘监听线程
        """
        hook(self.callback)
        wait()

    def play_key(self, key: str):
        """
        发声音一次
        :param key: 键位
        :return:
        """
        if self.lyre == 1:
            playsound("..\\sound\\FengWu\\" + key + ".mp3")
        elif self.lyre == 2:
            playsound("..\\sound\\LaoJiu\\" + key + ".mp3")
        elif self.lyre == 3:
            playsound("..\\sound\\JingHua\\" + key + ".mp3")

    def play_sound(self, key: str):
        """
        自动创建放声音的线程
        :param key: 键位
        :return:
        """
        t = Thread(target=self.play_key, args=key)
        t.daemon = True
        t.start()

    def callback(self, event):
        """
        监听键盘事件
        :param event:
        :return:
        """
        if not self.state:
            return
        event.name = event.name[0].upper() + event.name[1:]
        if event.event_type == 'down' and event.name in PlaySound.keyList:
            # print("[" + event.name + "]", end=",")
            self.play_sound(event.name)

    def start(self):
        """
        开启琴
        """
        self.state = True

    def stop(self):
        """
        关闭琴
        """
        self.state = False

    def setLyre(self, lyre: int):
        """
        设置琴的类型
        :param lyre: 琴的类型；1：风物、2：老旧、3：镜花
        """
        self.lyre = lyre
