import pyautogui
import time

# 歌词列表
lyrics = [
    "Verse 1: This is the first line",
    "Verse 1: This is the second line",
    "Chorus: This is the chorus",
    "Verse 2: Another verse"
]

# 设置文本位置
text_x = pyautogui.center(pyautogui.size())[0]
text_y = pyautogui.center(pyautogui.size())[1]

# 显示歌词
for lyric in lyrics:
    # 清空屏幕
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')

    # 显示歌词
    pyautogui.typewrite(lyric, interval=0.1)
    time.sleep(2)  # 此处可根据需要调整显示时间

# 关闭歌词显示
pyautogui.alert(text='Lyrics display finished', title='Message', button='OK')