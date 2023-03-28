# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/28
# @ Time 18:52
from time import sleep
from Lib.PlaySound import PlaySound

playSound = PlaySound()
playSound.start()
print("开启琴")
sleep(10)
playSound.stop()
print("关闭琴")
sleep(10)
