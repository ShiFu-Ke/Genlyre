# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/29
# @ Time 16:51
from os import listdir


class KeyMappingUtil:
    """
    键盘映射工具类
    """

    def __init__(self):
        self.mapping = {
            "鼠标左键": "LButton",
            "鼠标右键": "RButton",
            "鼠标中键": "MButton",
            "鼠标第四按键": "XButton1",
            "鼠标第五按键": "XButton2",
            "滚轮向下": "WheelDown",
            "滚轮向上": "WheelUp",
            "滚轮向左": "WheelLeft",
            "滚轮向右": "WheelRight",
            "大小写锁定键": "CapsLock",
            "空格键": "Space",
            "Tab键": "Tab",
            "回车键": "Enter",
            "退出键": "Escape",
            "退格键": "Backspace",
            "滚动锁定键": "ScrollLock",
            "删除键": "Delete",
            "插入改写切换键": "Insert",
            "Home键": "Home",
            "End键": "End",
            "向上翻页键": "PgUp",
            "向下翻页键": "PgDn",
            "向上方向键": "Up",
            "向下方向键": "Down",
            "向左方向键": "Left",
            "向右方向键": "Right",
            "小键盘开关": "NumLock",
            "小键盘0": "Numpad0",
            "小键盘1": "Numpad1",
            "小键盘2": "Numpad2",
            "小键盘3": "Numpad3",
            "小键盘4": "Numpad4",
            "小键盘5": "Numpad5",
            "小键盘6": "Numpad6",
            "小键盘7": "Numpad7",
            "小键盘8": "Numpad8",
            "小键盘9": "Numpad9",
            "小键盘除": "NumpadDiv",
            "小键盘乘": "NumpadMult",
            "小键盘加": "NumpadAdd",
            "小键盘减": "NumpadSub",
            "小键盘回车": "NumpadEnter",
            "左Windows": "LWin",
            "右Windows": "RWin",
            "左Ctrl": "LCtrl",
            "右Ctrl": "RCtrl",
            "左Shift": "LShift",
            "右Shift": "RShift",
            "左Alt": "LAlt",
            "右Alt": "RAlt",
            "后退": "Browser_Back",
            "前进": "Browser_Forward",
            "刷新": "Browser_Refresh",
            "停止": "Browser_Stop",
            "搜索": "Browser_Search",
            "收藏夹": "Browser_Favorites",
            "主页": "Browser_Home",
            "静音": "Volume_Mute",
            "调低音量": "Volume_Down",
            "增加音量": "Volume_Up",
            "下一首": "Media_Next",
            "上一首": "Media_Prev",
            "媒体停止": "Media_Stop",
            "Play/Pause": "Media_Play_Pause",
            "电子邮件": "Launch_Mail",
            "播放器": "Launch_Media",
            "此电脑": "Launch_App1",
            "计算器": "Launch_App2",
            "菜单键": "AppsKey",
            "捕获屏幕": "PrintScreen",
            "休眠键": "Sleep",
        }
        self.key = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z",
                    "X", "C", "V", "B", "N", "M", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "[", "]",
                    "\'", "\\", ",", ".", "/"]
        self.key += self.mapping.values()

    @staticmethod
    def getCfgFiles():
        """
        读取配置文件列表
        :return:键盘映射配置文件名称
        """
        arr = listdir("..\\keyMap\\")
        # 筛选文件格式并去掉后缀
        cfgList = []
        for i in arr:
            if i[-4:] == ".ahk":
                cfgList.append(i[:-4])
        # 将默认配置文件放在第一个位置
        i = cfgList.index("default")
        tmp = cfgList[i]
        cfgList[i] = cfgList[0]
        cfgList[0] = tmp
        return cfgList

    @staticmethod
    def newCfgFile(fileName):
        """
        新建配置文件
        :return:[成功返回True、否则返回False,提示信息]
        """
        if fileName in KeyMappingUtil.getCfgFiles():
            return False, "配置已存在！"
        try:
            file = open("..\\keyMap\\" + fileName + ".ahk", 'w', encoding="UTF-8")
            file.close()
            return True, "创建成功！"
        except Exception:
            return False, "文件名不能包含下列任意字符:\n\\/:*?\"<>|"

    def getKey(self, val):
        """
        获取键
        :param val: 值
        :return: 键，没有返回None
        """
        for key, value in self.mapping.items():
            if val == value:
                return key
        if val in self.key:
            return val

    def getValue(self, key):
        """
        获取值
        :param key: 键
        :return: 值，没有返回None
        """
        val = self.mapping.get(key)
        if val is None and key in self.key:
            return key
        return val

    def getMapping(self, fileName: str):
        """
        获取映射列表
        :param fileName: 文件名称
        :return: 用户视图下要显示的映射关系二维列表
        """
        file = open("..\\keyMap\\" + fileName + ".ahk", encoding='utf-8')
        arr = file.readlines()
        arrMap = []
        for i in arr:
            arr_tmp = i.replace("\n", "").split("::")
            if len(arr_tmp) != 2:
                continue
            arr_tmp[0] = self.getKey(arr_tmp[0])
            arr_tmp[1] = self.getKey(arr_tmp[1])
            if arr_tmp[0] is None or arr_tmp[1] is None:
                continue
            arrMap.append(arr_tmp.copy())
        return arrMap

    def setMapping(self, fileName: str, arrMap):
        """
        设置键盘映射配置文件
        :param fileName:文件名称
        :param arrMap: 用户视图下映射关系二维数组
        """
        test = ""
        for i, j in arrMap:
            i = self.getValue(i)
            j = self.getValue(j)
            if i is None or j is None:
                continue
            test += i + "::" + j + "\n"
        file = open("..\\keyMap\\" + fileName + ".ahk", 'w', encoding="UTF-8")
        file.write(test)
        file.close()


k = KeyMappingUtil()
print(k.newCfgFile("test")[1])
