from os import path
from os import path
from winreg import OpenKey, HKEY_CURRENT_USER, QueryValueEx

import pywin32_testutil
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QFileDialog

from Lib.MusicTest import MusicTest
from qfluentwidgets import (PrimaryPushButton, ComboBox, InfoBar, InfoBarPosition, TextEdit, DoubleSpinBox)
from util.ConfigUtil import ConfigUtil
from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class WriteScoresInterface(GalleryInterface):
    key = ["Q", "W", "E", "R", "T", "Y", "U", "A", "S", "D", "F", "G", "H", "J", "Z", "X", "C", "V", "B", "N", "M"]

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.writeScores,
            subtitle=t.writeScoresTitle,
            parent=parent
        )
        # 局部变量
        self.musicTest = MusicTest()
        self.lyre = 1
        self.pAdd = 0
        self.textLen = 0

        # 文字
        label_lyre = self.myLabel("Select lyre:")
        label_play = self.myLabel("Play:")
        # 下拉框
        self.comboBox_lyre = ComboBox()  # 琴谱格式
        self.comboBox_lyre.addItems([self.tr("Windsong Lyre"), self.tr('Vintage Lyre'), self.tr("Floral Zither")])
        self.comboBox_lyre.setCurrentIndex(0)
        self.comboBox_lyre.setMinimumWidth(140)
        self.comboBox_lyre.currentIndexChanged.connect(lambda: self.setLyre())
        # 按钮
        w = 110
        self.button_PlayAll = PrimaryPushButton(self.tr("Play all"))
        self.button_PlayAll.setMinimumWidth(w)
        self.button_PlayAll.clicked.connect(lambda: self.PlayAll())
        self.button_PlayCursor = PrimaryPushButton(self.tr("Play cursor"))
        self.button_PlayCursor.setMinimumWidth(w)
        self.button_PlayCursor.clicked.connect(lambda: self.PlayCursor())
        self.button_PlaySelect = PrimaryPushButton(self.tr("Play select"))
        self.button_PlaySelect.setMinimumWidth(w)
        self.button_PlaySelect.clicked.connect(lambda: self.PlaySelect())
        self.button_PlayStop = PrimaryPushButton(self.tr("Stop playing"))
        self.button_PlayStop.setMinimumWidth(w)
        self.button_PlayStop.clicked.connect(lambda: self.PlayStop())

        # 创建水平布局并放入组件
        HLayout_title = QHBoxLayout()
        HLayout_title.setSpacing(5)
        HLayout_title.addWidget(label_lyre)
        HLayout_title.addWidget(self.comboBox_lyre)
        HLayout_title.addStretch(1)
        HLayout_title.addWidget(label_play)
        HLayout_title.addWidget(self.button_PlayAll)
        HLayout_title.addWidget(self.button_PlayCursor)
        HLayout_title.addWidget(self.button_PlaySelect)
        HLayout_title.addWidget(self.button_PlayStop)

        # 文字
        label_speed = self.myLabel("Speed:")
        label_pADD = self.myLabel("Arpeggio acceleration:")
        # 可调大小的文本框
        self.doubleSpinBox = DoubleSpinBox(self)
        self.doubleSpinBox.setMinimumWidth(140)
        self.doubleSpinBox.setValue(0.6)  # 设置初始值为0.6
        # 下拉框
        self.comboBox_pADD = ComboBox()  # 琶音加速
        self.comboBox_pADD.addItems([str(i) for i in range(10)])
        self.comboBox_pADD.setCurrentIndex(0)
        self.comboBox_pADD.setMinimumWidth(10)
        self.comboBox_pADD.currentIndexChanged.connect(lambda: self.setPaDD())
        # 按钮
        self.button_Output = PrimaryPushButton(self.tr("Output"))
        self.button_Output.setMinimumWidth(w)
        self.button_Output.clicked.connect(lambda: self.Output())
        # 创建水平布局并放入组件
        HLayout_speed = QHBoxLayout()
        HLayout_speed.setSpacing(5)
        HLayout_speed.addWidget(label_speed)
        HLayout_speed.addWidget(self.doubleSpinBox)
        HLayout_speed.addWidget(label_pADD)
        HLayout_speed.addWidget(self.comboBox_pADD)
        HLayout_speed.addStretch(1)
        HLayout_speed.addWidget(self.button_Output)

        # 创建文本框
        self.textEdit = TextEdit(self)
        self.textEdit.setFixedHeight(410)  # 设置文本框高度
        self.textEdit.textChanged.connect(lambda: self.textChang())  # 监听文本框变化

        # 将水平布局加入页面
        self.vBoxLayout.addLayout(HLayout_title)
        self.vBoxLayout.addLayout(HLayout_speed)
        # 将文本框直接加入页面
        self.vBoxLayout.addWidget(self.textEdit)

    def myLabel(self, text):
        """
        创建label
        :param text:
        :return:
        """
        label = QLabel(self.tr(text))
        label.setObjectName('sourcePathLabel')  # 风格设置
        return label

    def setLyre(self):
        self.lyre = self.comboBox_lyre.currentIndex() + 1

    def setPaDD(self):
        self.pAdd = self.comboBox_pADD.currentIndex()

    def textChang(self):
        text = self.textEdit.toPlainText()
        if len(text) < self.textLen:
            self.textLen = len(text)
            return
        self.textLen = len(text)
        index = self.textEdit.textCursor().position()
        if len(text) < index or index < 1:
            return
        try:
            tmp = index
            while True:
                if text[tmp] in [")", "]"]:
                    return
                tmp += 1
        except Exception:
            pass
        if text[index - 1] == "(":
            self.textEdit.insertPlainText(")")
            cursor = self.textEdit.textCursor()
            cursor.setPosition(cursor.position() - 1)
            self.textEdit.setTextCursor(cursor)
        elif text[index - 1] == "[":
            self.textEdit.insertPlainText("]")
            cursor = self.textEdit.textCursor()
            cursor.setPosition(cursor.position() - 1)
            self.textEdit.setTextCursor(cursor)

    def PlayAll(self):
        text = str(self.doubleSpinBox.value()) + "\n" + self.textEdit.toPlainText()
        self.playBegin(text)

    def PlayCursor(self):
        text = str(self.doubleSpinBox.value()) + "\n" + self.textEdit.toPlainText()[
                                                        self.textEdit.textCursor().position():]
        self.playBegin(text)

    def PlaySelect(self):
        text = str(self.doubleSpinBox.value()) + "\n" + self.textEdit.textCursor().selectedText()
        self.playBegin(text)

    def PlayStop(self):
        self.musicTest.finish()

    def Output(self):
        url = ConfigUtil.rYaml("writeScoresInterface", "savePath")
        if url is None or not path.isdir(url):
            key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
            url = QueryValueEx(key, "Desktop")[0]
        # 显示文件对话框，让用户选择要保存的文件和位置
        filename, _ = QFileDialog.getSaveFileName(self, self.tr("Save music score"), url + "/俺の琴谱（脚本琴谱）.txt",
                                                  self.tr("Music score") + " (*.txt)")
        # 如果用户选择了文件路径，则进行保存操作
        if filename:
            ConfigUtil.wYaml(filename[:filename.rfind("/")], "writeScoresInterface", "savePath")
            text = str(self.doubleSpinBox.value()) + "\n" + self.textEdit.toPlainText()
            with open(filename, 'w') as f:
                f.write(text)
            InfoBar.success(
                title=self.tr('Remind'),
                content=self.tr("Save success"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,  # won't disappear automatically
                parent=self
            )

    def playBegin(self, text):
        # 排除出错符号
        while text[-1] in ["", "\n", "-", "+"]:
            text = text[:-1]
        # 如果所有字符不在key中，return
        for i in text:
            if i in WriteScoresInterface.key or i in [str(k) for k in range(1, 8)]:
                break
        else:
            return
        print(MusicTest.isKe(text)[1])
        if not MusicTest.isKe(text)[0]:
            InfoBar.error(
                title=self.tr('Remind'),
                content=self.tr("Please check that your parentheses match"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,  # won't disappear automatically
                parent=self
            )
            return
        self.musicTest.start(text, self.lyre, self.pAdd)
