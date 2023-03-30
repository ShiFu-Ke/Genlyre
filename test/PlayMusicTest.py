# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/19
# @ Time 21:16

from Lib.PlayMusic import PlayMusic
from time import sleep
from Lib.MusicScore import MusicScore

path = "..\\testRes\\铃芽之旅(ke).txt"  # 刻师傅谱路径
# path = "..\\testRes\\打上花火(gua).txt"  # 呱呱谱路径


sleep(3)
playMusic = PlayMusic()
playMusic.start(path, 1, 1)  # 开始
sleep(10)
playMusic.suspend_continue()  # 暂停
sleep(3)
playMusic.suspend_continue()  # 继续
sleep(10)
playMusic.finish()  # 结束
