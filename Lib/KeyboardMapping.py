# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/19
# @ Time 22:34
from os import system


class KeyboardMapping:
    """
    键盘映射类
    """

    def start(self, fileName):
        system("..\\bin\\AutoHotkey.exe ..\\keyMap\\%s.ahk &" % fileName)


k = KeyboardMapping()
k.start("text")
