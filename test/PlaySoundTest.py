# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/28
# @ Time 18:52
from time import sleep
from Lib.PlaySound import PlaySound

playSound = PlaySound()

playSound.setLyre(2)
print("设置琴为老旧")

playSound.start()
print("开启琴")

sleep(3000)

playSound.stop()
print("关闭琴")

sleep(5)

playSound.start()
print("开启琴")

playSound.setLyre(1)
print("设置琴为风物")

sleep(30)

playSound.setLyre(3)
print("设置琴为镜花")

sleep(30)

playSound.stop()
print("关闭琴")

sleep(5)
