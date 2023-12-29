# @ Created with PyCharm Professional 2021.2.1
# @ Author KeShiFu
# @ Date 2023/09/06
# @ Time 16:58
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER

from Lib.MusicScore import MusicScore
from Lib.midi import Midi

from win32ui import CreateFileDialog


def get_desktop():
    key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return QueryValueEx(key, "Desktop")[0]


try:
    input("欢迎使用此脚本，内测版请勿外传！\n原琴玩家刻师傅：简谱大师导出mid文件时记得选中”播放用“；如果简谱中存在三连音、琶音等特殊音符，"
          "可能会转换失败或可读性极差0.0\n按下回车选择文件......")
    # 选择文件
    lpsFilter = "mid Files (*.mid)|*.mid|"
    dlg = CreateFileDialog(True, "mid", None, 0x04 | 0x02, lpsFilter)  # 1表⽰打开⽂件对话框
    dlg.SetOFNInitialDir(get_desktop())  # 设置打开⽂件对话框中的初始显⽰⽬录
    dlg.DoModal()
    filename = dlg.GetPathName()  # 获取选择的⽂件名称
    if filename[-3:] != "mid":
        exit(1)
    rev = input("同时按的按键顺序是否翻转[y/n]:")
    if rev.upper() == "Y":
        rev = True
    else:
        rev = False
    bar = int(input("每小节几拍(如4)："))
    pat = int(input("几分音符为一拍(如4)："))
    shotPat = int(input("简谱中最短音长为几分音符(如16)："))
    tmp = Midi.get_keys(filename, rev)
    gua = str(int(tmp[1] * 250)) + "\n" + tmp[0]
    ke = MusicScore.guaToke(gua, bar, pat, shotPat)
    file_out = open(filename[:-4] + ".txt", 'w', encoding="UTF-8")
    file_out.write(ke)
    file_out.close()
    print("转换成功！")
except Exception as e:
    print("error!!!!!!!!!!!!!")
input("反馈请联系刻师傅，按回车或直接关闭！")
