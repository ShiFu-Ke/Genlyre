# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/04/15
# @ Time 20:36
import zhconv

b = [
    "Quick jump", "Auto play", "Music score conversion", "Write music scores", "Lyre", "Keyboard Mapping",
    "After importing the score, it can be played automatically.",
    "You can convert the music score to the desired format from here.",
    "You can conveniently write music scores here.",
    "You can play the piano here.",
    "You can set keyboard mapping while playing."
]
a = [
    "快速跳转", "自动演奏", "琴谱转换", "扒谱工具", "模拟原琴", "键盘映射",
    "导入琴谱后可以自动演奏。",
    "你可以从这里将琴谱转换成想要的格式。",
    "你可以这里方便的扒谱。",
    "你可以在这里弹琴。",
    "你在演奏的时候可以设置键盘映射。"
]
tmp = 0
text = "../../view/home_interface.py"

l = tmp
for i, j in zip(a, b):
    print("""   <message>
        <location filename=\"""" + text + """\" line=\"""" + str(l + 1) + """\"/>
        <source>""" + j + """</source>
        <translation>""" + zhconv.convert(i, 'zh-hant') + """</translation>
    </message>""")
    l += 1
l = tmp
print("\n\n\n\n")
for i, j in zip(a, b):
    print("""   <message>
        <location filename=\"""" + text + """\" line=\"""" + str(l + 1) + """\"/>
        <source>""" + j + """</source>
        <translation>""" + i + """</translation>
    </message>""")
    l += 1
