# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/04/15
# @ Time 20:36
import zhconv

b = [
    "Settings",
]
a = [
    "伊蕾娜",
]
tmp = 29
text = "../../view/main_window.py"

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
