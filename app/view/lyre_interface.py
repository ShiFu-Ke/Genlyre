from threading import Thread
from PyQt5.QtCore import QSize, QSequentialAnimationGroup, QEasingCurve, QPropertyAnimation, QRect, Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel
from keyboard import add_hotkey, remove_all_hotkeys
from playsound import playsound

from qfluentwidgets import (ToolButton, ComboBox, SwitchButton)
from util.ConfigUtil import ConfigUtil
from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class LyreInterface(GalleryInterface):
    key = ["Q", "W", "E", "R", "T", "Y", "U", "A", "S", "D", "F", "G", "H", "J", "Z", "X", "C", "V", "B", "N", "M"]
    key_map = {
        "65": "A", "66": "B", "67": "C", "68": "D", "69": "E", "70": "F", "71": "G", "72": "H", "74": "J", "77": "M",
        "78": "N", "81": "Q", "82": "R", "83": "S", "84": "T", "85": "U", "86": "V", "87": "W", "88": "X", "89": "Y",
        "90": "Z"
    }

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.lyre,
            subtitle=t.lyreTitle,
            parent=parent
        )
        # 局部变量
        self.size = 70
        self.lyre = 1  # 1:风物；2：老旧；3：镜花

        # 开关和琴类型
        label_lyre = self.myLabel("Select lyre:")
        label_switch = self.myLabel("Shortcut keys:")
        # 下拉框
        self.comboBox_lyre = ComboBox()  # 琴谱格式
        self.comboBox_lyre.addItems([self.tr("Windsong Lyre"), self.tr('Vintage Lyre'), self.tr("Floral Zither")])
        self.comboBox_lyre.setCurrentIndex(0)
        self.comboBox_lyre.setMinimumWidth(140)
        self.comboBox_lyre.currentIndexChanged.connect(lambda: self.setLyre())
        # 开关
        self.switchButton = SwitchButton(self.tr('Off'))
        self.switchButton.checkedChanged.connect(self.onSwitchCheckedChanged)
        # 创建水平布局
        HLayout_title = QHBoxLayout()
        HLayout_title.addWidget(label_lyre)
        HLayout_title.addWidget(self.comboBox_lyre)
        HLayout_title.addStretch(1)
        # HLayout_title.addWidget(label_switch)
        # HLayout_title.addWidget(self.switchButton)
        # 创建21个带图标的按钮
        self.buttons = self.newToolButtons()
        # 将按钮放入三个水平布局
        HLayout_key01 = QHBoxLayout()
        HLayout_key01.addStretch(1)
        for i in range(0, 6):
            HLayout_key01.addWidget(self.buttons[i])
        HLayout_key01.addStretch(1)
        HLayout_key02 = QHBoxLayout()
        HLayout_key02.addStretch(1)
        for i in range(7, 13):
            HLayout_key02.addWidget(self.buttons[i])
        HLayout_key02.addStretch(1)
        HLayout_key03 = QHBoxLayout()
        HLayout_key03.addStretch(1)
        for i in range(14, 20):
            HLayout_key03.addWidget(self.buttons[i])
        HLayout_key03.addStretch(1)

        # 将水平布局放入页面
        self.vBoxLayout.addLayout(HLayout_title)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addLayout(HLayout_key01)
        self.vBoxLayout.addLayout(HLayout_key02)
        self.vBoxLayout.addLayout(HLayout_key03)
        self.vBoxLayout.addStretch(1)

        # if ConfigUtil.rYaml("lyre", "key") == 1:
        #     self.switchButton.setChecked(True)
        #     self.onSwitchCheckedChanged(self.switchButton)

    def keyPressEvent(self, event):
        key = self.key_map.get(str(event.key()))
        if key is None:
            return
        self.playKey(key)

    def setLyre(self):
        if self.comboBox_lyre.currentIndex() == 0:
            self.lyre = 1
            for i in range(len(self.buttons)):
                self.buttons[i].setIcon('app/resource/img/FengWu/' + self.key[i] + '.png')
        elif self.comboBox_lyre.currentIndex() == 1:
            self.lyre = 2
            for i in range(len(self.buttons)):
                self.buttons[i].setIcon('app/resource/img/LaoJiu/' + self.key[i] + '.png')
        elif self.comboBox_lyre.currentIndex() == 2:
            self.lyre = 3
            for i in range(len(self.buttons)):
                self.buttons[i].setIcon('app/resource/img/JingHua/' + self.key[i] + '.png')

    def newToolButtons(self):
        arr = []
        button_Q = ToolButton('app/resource/img/FengWu/' + self.key[0] + '.png')
        button_Q.clicked.connect(lambda: self.playKey(self.key[0]))
        arr.append(button_Q)
        button_W = ToolButton('app/resource/img/FengWu/' + self.key[1] + '.png')
        button_W.clicked.connect(lambda: self.playKey(self.key[1]))
        arr.append(button_W)
        button_E = ToolButton('app/resource/img/FengWu/' + self.key[2] + '.png')
        button_E.clicked.connect(lambda: self.playKey(self.key[2]))
        arr.append(button_E)
        button_R = ToolButton('app/resource/img/FengWu/' + self.key[3] + '.png')
        button_R.clicked.connect(lambda: self.playKey(self.key[3]))
        arr.append(button_R)
        button_T = ToolButton('app/resource/img/FengWu/' + self.key[4] + '.png')
        button_T.clicked.connect(lambda: self.playKey(self.key[4]))
        arr.append(button_T)
        button_Y = ToolButton('app/resource/img/FengWu/' + self.key[5] + '.png')
        button_Y.clicked.connect(lambda: self.playKey(self.key[5]))
        arr.append(button_Y)
        button_U = ToolButton('app/resource/img/FengWu/' + self.key[6] + '.png')
        button_U.clicked.connect(lambda: self.playKey(self.key[6]))
        arr.append(button_U)
        button_A = ToolButton('app/resource/img/FengWu/' + self.key[7] + '.png')
        button_A.clicked.connect(lambda: self.playKey(self.key[7]))
        arr.append(button_A)
        button_S = ToolButton('app/resource/img/FengWu/' + self.key[8] + '.png')
        button_S.clicked.connect(lambda: self.playKey(self.key[8]))
        arr.append(button_S)
        button_D = ToolButton('app/resource/img/FengWu/' + self.key[9] + '.png')
        button_D.clicked.connect(lambda: self.playKey(self.key[9]))
        arr.append(button_D)
        button_F = ToolButton('app/resource/img/FengWu/' + self.key[10] + '.png')
        button_F.clicked.connect(lambda: self.playKey(self.key[10]))
        arr.append(button_F)
        button_G = ToolButton('app/resource/img/FengWu/' + self.key[11] + '.png')
        button_G.clicked.connect(lambda: self.playKey(self.key[11]))
        arr.append(button_G)
        button_H = ToolButton('app/resource/img/FengWu/' + self.key[12] + '.png')
        button_H.clicked.connect(lambda: self.playKey(self.key[12]))
        arr.append(button_H)
        button_J = ToolButton('app/resource/img/FengWu/' + self.key[13] + '.png')
        button_J.clicked.connect(lambda: self.playKey(self.key[13]))
        arr.append(button_J)
        button_Z = ToolButton('app/resource/img/FengWu/' + self.key[14] + '.png')
        button_Z.clicked.connect(lambda: self.playKey(self.key[14]))
        arr.append(button_Z)
        button_X = ToolButton('app/resource/img/FengWu/' + self.key[15] + '.png')
        button_X.clicked.connect(lambda: self.playKey(self.key[15]))
        arr.append(button_X)
        button_C = ToolButton('app/resource/img/FengWu/' + self.key[16] + '.png')
        button_C.clicked.connect(lambda: self.playKey(self.key[16]))
        arr.append(button_C)
        button_V = ToolButton('app/resource/img/FengWu/' + self.key[17] + '.png')
        button_V.clicked.connect(lambda: self.playKey(self.key[17]))
        arr.append(button_V)
        button_B = ToolButton('app/resource/img/FengWu/' + self.key[18] + '.png')
        button_B.clicked.connect(lambda: self.playKey(self.key[18]))
        arr.append(button_B)
        button_N = ToolButton('app/resource/img/FengWu/' + self.key[19] + '.png')
        button_N.clicked.connect(lambda: self.playKey(self.key[19]))
        arr.append(button_N)
        button_M = ToolButton('app/resource/img/FengWu/' + self.key[20] + '.png')
        button_M.clicked.connect(lambda: self.playKey(self.key[20]))
        arr.append(button_M)
        for i in arr:
            i.setIconSize(QSize(self.size, self.size))
        return arr

    def playKey(self, key):
        if self.lyre == 1:
            Thread(daemon=True, target=lambda: self.playAKey("app/resource/sound/FengWu/" + key + ".wav")).start()
        elif self.lyre == 2:
            Thread(daemon=True, target=lambda: self.playAKey("app/resource/sound/LaoJiu/" + key + ".wav")).start()
        else:
            Thread(daemon=True, target=lambda: self.playAKey("app/resource/sound/JingHua/" + key + ".wav")).start()

    @staticmethod
    def playAKey(key):
        playsound(key)

    def myLabel(self, text):
        """
        创建label
        :param text:
        :return:
        """
        label = QLabel(self.tr(text))
        label.setObjectName('sourcePathLabel')  # 风格设置
        return label

    def onSwitchCheckedChanged(self, isChecked):
        if isChecked:
            self.switchButton.setText(self.tr('On'))
            ConfigUtil.wYaml(1, "lyre", "key")
            add_hotkey(self.key[0], lambda: self.buttons[0].click())
            add_hotkey(self.key[1], lambda: self.buttons[1].click())
            add_hotkey(self.key[2], lambda: self.buttons[2].click())
            add_hotkey(self.key[3], lambda: self.buttons[3].click())
            add_hotkey(self.key[4], lambda: self.buttons[4].click())
            add_hotkey(self.key[5], lambda: self.buttons[5].click())
            add_hotkey(self.key[6], lambda: self.buttons[6].click())
            add_hotkey(self.key[7], lambda: self.buttons[7].click())
            add_hotkey(self.key[8], lambda: self.buttons[8].click())
            add_hotkey(self.key[9], lambda: self.buttons[9].click())
            add_hotkey(self.key[10], lambda: self.buttons[10].click())
            add_hotkey(self.key[11], lambda: self.buttons[11].click())
            add_hotkey(self.key[12], lambda: self.buttons[12].click())
            add_hotkey(self.key[13], lambda: self.buttons[13].click())
            add_hotkey(self.key[14], lambda: self.buttons[14].click())
            add_hotkey(self.key[15], lambda: self.buttons[15].click())
            add_hotkey(self.key[16], lambda: self.buttons[16].click())
            add_hotkey(self.key[17], lambda: self.buttons[17].click())
            add_hotkey(self.key[18], lambda: self.buttons[18].click())
            add_hotkey(self.key[19], lambda: self.buttons[19].click())
            add_hotkey(self.key[20], lambda: self.buttons[20].click())
        else:
            remove_all_hotkeys()
            ConfigUtil.wYaml(0, "lyre", "key")
            self.switchButton.setText(self.tr('Off'))
