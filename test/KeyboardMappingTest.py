# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/20
# @ Time 22:23
from time import sleep

from Lib.KeyboardMapping import KeyboardMapping

keyboardMapping = KeyboardMapping()  # 创建对象
keyboardMapping.start("..\\")  # 调用开启键盘映射成员方法
sleep(20)
keyboardMapping.stop()  # 调用结束映射成员方法
