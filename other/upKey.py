# @ Created with PyCharm Professional 2021.2.1
# @ Author KeShiFu
# @ Date 2023/12/29
# @ Time 14:49
from winreg import HKEY_CURRENT_USER, QueryValueEx, OpenKey

from win32ui import CreateFileDialog


def get_desktop():
    key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return QueryValueEx(key, "Desktop")[0]


lpsFilter = "键盘谱 (*.txt)|*.txt|"
dlg = CreateFileDialog(True, "txt", None, 0x04 | 0x02, lpsFilter)  # 1表⽰打开⽂件对话框
dlg.SetOFNInitialDir(get_desktop())  # 设置打开⽂件对话框中的初始显⽰⽬录
dlg.DoModal()
filename = dlg.GetPathName()  # 获取选择的⽂件名称
file = open(filename, encoding='utf-8')
data = file.read()
file.close()

key1 = "QWERTYUASDFGHJZXCVBNM"
key2 = "1234567QWERTYUASDFGHJ"
endData = ""
for i in data:
    try:
        endData += key2[key1.index(i)]
    except:
        endData += i

file_out = open(filename[:-4] + "(升调).txt", 'w', encoding="UTF-8")
file_out.write(endData)
file_out.close()
