import functools

from PyQt5.QtCore import Qt, QTime, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLabel

from Lib.KeyboardMapping import KeyboardMapping
from qfluentwidgets import (PrimaryPushButton, SwitchButton, InfoBar, InfoBarPosition, PickerBase, PickerPanel)
from util.ConfigUtil import ConfigUtil
from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class KeyMappingInterface(GalleryInterface):
    key = ["Q", "W", "E", "R", "T", "Y", "U", "A", "S", "D", "F", "G", "H", "J", "Z", "X", "C", "V", "B", "N", "M"]

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.keyMapping,
            subtitle=t.keyMappingTitle,
            parent=parent
        )
        # 局部变量
        self.arr_mapping = []  # 放映射组件（二维）
        self.arr_HLayout = []
        self.arr_module = []
        self.keyboardMapping = KeyboardMapping()  # 映射对象

        # 文字
        label_onf = self.myLabel("Keyboard mapping switch")
        # 开关
        self.switchButton = SwitchButton(self.tr('Off'))
        self.switchButton.checkedChanged.connect(self.onSwitchCheckedChanged)
        # 添加映射的按钮
        self.add_button = PrimaryPushButton(self.tr("Add"))
        self.add_button.clicked.connect(lambda: self.addMapping())
        # 更新映射的按钮
        self.update_button = PrimaryPushButton(self.tr("Update"))
        self.update_button.clicked.connect(lambda: self.update_cfg())

        # 创建水平布局并添加组件
        HLayout_title = QHBoxLayout()
        HLayout_title.setSpacing(10)
        HLayout_title.addWidget(label_onf)
        HLayout_title.addWidget(self.switchButton)
        HLayout_title.addStretch(1)
        HLayout_title.addWidget(self.add_button)
        HLayout_title.addWidget(self.update_button)

        # 将水平布局添加到页面
        self.vBoxLayout.addLayout(HLayout_title)
        # 读取文件并创建对应关系
        self.init()
        if ConfigUtil.rYaml("keyMapping", "mapping") == 1:
            self.switchButton.setChecked(True)
            self.onSwitchCheckedChanged(self.switchButton)

    def init(self):
        file = open("data\\default.ahk", "r", encoding="utf-8")
        arr_keyMapping = list(map(lambda x: x.replace("\n", "").split("::"), list(file.readlines())))
        file.close()
        for i in arr_keyMapping:
            self.arr_mapping.append([i[0], i[1]])
        self.updateMapper(True)

    def updateMapper(self, add=False):
        """更新组件"""
        # 删除组件
        while len(self.arr_module) > 0:
            for i in self.arr_module[0]:
                i.deleteLater()
            self.arr_HLayout[0].deleteLater()
            self.arr_HLayout.pop(0)
            self.arr_module.pop(0)
        if not add:
            # 关闭映射
            self.keyboardMapping.stop()
            # 写配置文件
            file = open("data\\default.ahk", "w", encoding="utf-8")
            data = ""
            for i in self.arr_mapping:
                data += i[0] + "::" + i[1] + "\n"
            file.write(data)
            file.close()
            if ConfigUtil.rYaml("keyMapping", "mapping") == 1:
                self.keyboardMapping.start("")
        # 添加组件
        for i in self.arr_mapping:
            v1 = KeyPicker(self, i[0])
            label = self.myLabel("    -->    ")
            v2 = KeyPicker(self, i[1])
            button = PrimaryPushButton(self.tr("Delete mapping"))
            button.clicked.connect(functools.partial(self.delMapping, button))
            self.arr_module.append([v1, label, v2, button])
            HLayout = QHBoxLayout()
            HLayout.setSpacing(10)
            HLayout.addStretch(1)
            HLayout.addWidget(v1)
            HLayout.addWidget(label)
            HLayout.addWidget(v2)
            HLayout.addWidget(button)
            HLayout.addStretch(1)
            self.arr_HLayout.append(HLayout)
            self.vBoxLayout.addLayout(HLayout)

    def myLabel(self, text):
        """
        创建label
        :param text:
        :return:
        """
        label = QLabel(self.tr(text))
        label.setObjectName('sourcePathLabel')  # 风格设置
        return label

    def delMapping(self, button):
        """删除一组组件"""
        index = None
        for i in range(len(self.arr_module)):
            if button == self.arr_module[i][3]:
                index = i
        for i in self.arr_module[index]:
            i.deleteLater()
        self.arr_HLayout[index].deleteLater()
        self.arr_HLayout.pop(index)
        self.arr_module.pop(index)
        self.arr_mapping.pop(index)
        self.updateMapper()

    def addMapping(self):
        self.arr_mapping.insert(0, ["", ""])
        self.updateMapper(True)

    def update_cfg(self):
        self.arr_mapping.clear()
        for i in self.arr_module:
            if i[0].data is not None and i[2].data is not None:
                self.arr_mapping.append([i[0].data, i[2].data])
        self.updateMapper()
        InfoBar.success(
            title=self.tr('Remind'),
            content=self.tr("Update success"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,  # won't disappear automatically
            parent=self
        )

    def onSwitchCheckedChanged(self, isChecked):
        if isChecked:
            self.keyboardMapping.start("")
            ConfigUtil.wYaml(1, "keyMapping", "mapping")
            self.switchButton.setText(self.tr('On'))
        else:
            self.keyboardMapping.stop()
            ConfigUtil.wYaml(0, "keyMapping", "mapping")
            self.switchButton.setText(self.tr('Off'))


class KeyBase(PickerBase):
    """ Time picker base class """

    timeChanged = pyqtSignal(QTime)

    def __init__(self, parent=None, showSeconds=False):
        super().__init__(parent=parent)
        self.showSeconds = showSeconds
        self.time = QTime()

    def setTime(self, time: QTime):
        """ set current time

        Parameters
        ----------
        time: QTime
            current time
        """
        raise NotImplementedError

    def setSecondVisible(self, isVisible: bool):
        """ set the visibility of seconds column """
        raise NotImplementedError


class KeyPicker(KeyBase):
    """ 选择框 """

    def __init__(self, k, key):
        parent = None
        showSeconds = False
        super().__init__(parent, showSeconds)
        self.data = None
        self.k = k
        self.keyType = ['mouse', 'keyboard', 'Keypad', 'Function keys', 'cursor control', 'Key modifier', 'multi-media',
                        'Special keys']
        self.key = [['LButton', 'RButton', 'MButton', 'XButton1', 'XButton2', 'WheelDown', 'WheelUp', 'WheelLeft',
                     'WheelRight'],
                    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
                     'x', 'c',
                     'v', 'b', 'n', 'm', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '[', ']', '\\',
                     "'", ',', '.',
                     '/'],
                    ['NumLock', 'Numpad0', 'Numpad1', 'Numpad2', 'Numpad3', 'Numpad4', 'Numpad5', 'Numpad6', 'Numpad7',
                     'Numpad8',
                     'Numpad9', 'NumpadDiv', 'NumpadMult', 'NumpadAdd', 'NumpadSub', 'NumpadEnter'],
                    ['CapsLock', 'Space', 'Tab', 'Enter', 'Escape', 'Backspace', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6',
                     'F7', 'F8',
                     'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22',
                     'F23', 'F24'],
                    ['ScrollLock', 'Delete', 'Insert', 'Home', 'End', 'PgUp', 'PgDn', 'Up', 'Left', 'Right'],
                    ['LWin', 'RWin', 'LCtrl', 'RCtrl', 'LShift', 'RShift', 'LAlt', 'RAlt'],
                    ['Browser_Back', 'Browser_Forward', 'Browser_Refresh', 'Browser_Stop', 'Browser_Search',
                     'Browser_Favorites',
                     'Browser_Home', 'Volume_Mute', 'Volume_Down', 'Volume_Up', 'Media_Next', 'Media_Prev',
                     'Media_Stop',
                     'Media_Play_Pause', 'Launch_Mail', 'Launch_Media', 'Launch_App1', 'Launch_App2'],
                    ['AppsKey', 'PrintScreen', 'Sleep']]
        self.w = 140
        # 添加按键类型
        self.addColumn(k.tr('Key type'), map(lambda x: self.k.tr(x), self.keyType), self.w)

        # 添加按键
        self.addColumn(k.tr('key'), map(lambda x: self.k.tr(x), self.key[0]), self.w)

        self.setValue(key)

    def setValue(self, key):
        for i in range(len(self.key)):
            if key in self.key[i]:
                self.setColumn(1, self.k.tr(key), list(map(lambda x: self.k.tr(x), self.key[i])), self.w)
                self.setColumnValue(0, self.k.tr(self.keyType[i]))
                self.setColumnValue(1, self.k.tr(key))
                self.data = key


    def _onColumnValueChanged(self, panel: PickerPanel, index, value):
        if index == 0:
            c = panel.column(1)
            c.setItems(
                list(map(lambda x: self.k.tr(x),
                         self.key[list(map(lambda x: self.k.tr(x), self.keyType)).index(value)])))

    def _onConfirmed(self, value: list):
        """确定后触发"""
        super()._onConfirmed(value)
        for i in range(len(self.key)):
            if value[1] in list(map(lambda x: self.k.tr(x), self.key[i])):
                self.data = self.key[i][list(map(lambda x: self.k.tr(x), self.key[i])).index(value[1])]
        self.setValue(self.data)
        InfoBar.info(
            title=self.k.tr('Remind'),
            content=self.k.tr("Please click on update"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,  # won't disappear automatically
            parent=self.k
        )
