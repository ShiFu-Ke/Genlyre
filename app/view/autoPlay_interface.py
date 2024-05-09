from os import path
from winreg import OpenKey, HKEY_CURRENT_USER, QueryValueEx

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QButtonGroup, QHBoxLayout, QLabel, QFileDialog
from pynput import keyboard

from Lib.MusicScore import MusicScore
from Lib.PlayMusic import PlayMusic
from qfluentwidgets import (PushButton, PrimaryPushButton, ComboBox, RadioButton, MessageBox, SpinBox)
from util.ConfigUtil import ConfigUtil
from util.PlayUtil import PlayUtil
from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class AutoPlayInterface(GalleryInterface):

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.autoPlay,
            subtitle=t.autoPlayTitle,
            parent=parent
        )
        # 局部变量
        self.key = ["None", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]
        self.songList = []  # [[完整路径，（0mid,1刻师傅,2呱呱,3伊蕾娜）],...]
        self.songListLength = len(self.songList)
        self.scoreType = 1  # 琴谱格式
        self.lyre = 1  # 琴的类型
        self.pADD = 0  # 琶音提速
        self.bufTime = 10  # 缓冲时间
        self.playMusic = PlayMusic()  # 创建演奏对象
        self.QKey = ["", "", ""]  # 快捷键保存位置[开始，暂停/继续，结束]
        self.listener = keyboard.Listener(on_press=self.on_press).start()
        # 快捷键设置
        # 文本
        label_key = self.myLabel("Shortcut key settings:")
        label_begin = self.myLabel("Begin:")
        label_pause_resume = self.myLabel("Pause/Resume:")
        label_cease = self.myLabel("Cease:")
        # 开始快捷键下拉框
        self.comboBox_begin = ComboBox()
        self.comboBox_begin.addItems(self.key)
        self.comboBox_begin.setCurrentIndex(0)
        self.comboBox_begin.setMinimumWidth(80)
        self.comboBox_begin.currentIndexChanged.connect(
            lambda: self.updateKey(self.comboBox_begin.currentText(), 1))
        # 暂停快捷键下拉框
        self.comboBox_pause_resume = ComboBox()  #
        self.comboBox_pause_resume.addItems(self.key)
        self.comboBox_pause_resume.setCurrentIndex(0)
        self.comboBox_pause_resume.setMinimumWidth(80)
        self.comboBox_pause_resume.currentIndexChanged.connect(
            lambda: self.updateKey(self.comboBox_pause_resume.currentText(), 2))
        # 停止快捷键下拉框
        self.comboBox_cease = ComboBox()
        self.comboBox_cease.addItems(self.key)
        self.comboBox_cease.setCurrentIndex(0)
        self.comboBox_cease.setMinimumWidth(80)
        self.comboBox_cease.currentIndexChanged.connect(
            lambda: self.updateKey(self.comboBox_cease.currentText(), 3))
        # 水平布局
        HLayout_key = QHBoxLayout()
        HLayout_key.setAlignment(Qt.AlignTop)
        HLayout_key.setSpacing(10)
        HLayout_key.addWidget(label_key, 0, Qt.AlignLeft)
        HLayout_key.addStretch(1)
        HLayout_key.addWidget(label_begin, 0, Qt.AlignLeft)
        HLayout_key.addWidget(self.comboBox_begin, 0, Qt.AlignLeft)
        HLayout_key.addWidget(label_pause_resume, 0, Qt.AlignRight)
        HLayout_key.addWidget(self.comboBox_pause_resume, 0, Qt.AlignLeft)
        HLayout_key.addWidget(label_cease, 0, Qt.AlignRight)
        HLayout_key.addWidget(self.comboBox_cease, 0, Qt.AlignLeft)

        # 导入琴谱
        # 文本
        label_MusicalScore = self.myLabel("Format of musical score:")
        # 下拉框
        self.comboBox_head = ComboBox()  # 琴谱格式
        # self.comboBox_head.addItems(
        #     [self.tr("Format of KeShiFu"), self.tr('Format of GuaGua'), self.tr('Format of YiLeiNa')])
        self.comboBox_head.addItems([self.tr("Format of KeShiFu"), self.tr('Format of GuaGua')])
        # self.comboBox_head.addItems([self.tr("Format of KeShiFu")])
        self.comboBox_head.setCurrentIndex(0)
        self.comboBox_head.setMinimumWidth(165)
        self.comboBox_head.currentIndexChanged.connect(lambda: self.setScoreType())
        # 按钮
        button_input = PushButton(self.tr('Input'))
        button_input.clicked.connect(lambda: self.addList())
        button_delete = PushButton(self.tr('Delete'))
        button_delete.clicked.connect(lambda: self.deleteSong())
        button_empty = PushButton(self.tr('Empty'))
        button_empty.clicked.connect(lambda: self.clearSong())

        # 中间单选框
        self.radioWidget = QWidget()
        self.radioLayout = QVBoxLayout(self.radioWidget)
        self.radioLayout.setContentsMargins(2, 0, 0, 0)
        self.radioLayout.setSpacing(15)
        self.buttonGroup = QButtonGroup(self.radioWidget)

        # 底部按钮
        # 文本
        label_SelectInstrument = self.myLabel("Select lyre:")
        label_pADD = self.myLabel("Arpeggio acceleration:")
        label_BufTime=self.myLabel("Buffer time:")
        # 下拉框
        self.comboBox_lyre = ComboBox()  # 琴谱格式
        self.comboBox_lyre.addItems([self.tr("Windsong Lyre"), self.tr('Vintage Lyre')])
        self.comboBox_lyre.setCurrentIndex(0)
        self.comboBox_lyre.setMinimumWidth(140)
        self.comboBox_lyre.currentIndexChanged.connect(lambda: self.setLyre())
        # 下拉框
        self.comboBox_pADD = ComboBox()  # 琶音加速
        self.comboBox_pADD.addItems([str(i) for i in range(10)])
        self.comboBox_pADD.setCurrentIndex(0)
        self.comboBox_pADD.setMinimumWidth(10)
        self.comboBox_pADD.currentIndexChanged.connect(lambda: self.setPaDD())
        # 可调大小数字框
        self.spinBox_bufTime = SpinBox(self)
        self.spinBox_bufTime.setRange(10, 200)
        self.spinBox_bufTime.setValue(self.bufTime)  # 设置初始值
        self.spinBox_bufTime.setSingleStep(5)  # 设置增量
        self.spinBox_bufTime.valueChanged.connect(lambda: self.setBufTime())

        # 按钮
        self.button_begin = PrimaryPushButton(self.tr('Begin'))
        self.button_begin.setMinimumWidth(135)
        self.button_begin.clicked.connect(lambda: self.start())
        self.button_pauseResume = PrimaryPushButton(self.tr('Pause/Resume'))
        self.button_pauseResume.setMinimumWidth(135)
        self.button_pauseResume.clicked.connect(lambda: self.playMusic.suspend_continue())
        self.button_cease = PrimaryPushButton(self.tr('Cease'))
        self.button_cease.setMinimumWidth(135)
        self.button_cease.clicked.connect(lambda: self.playMusic.finish())

        # 水平布局
        HLayout_head = QHBoxLayout()
        HLayout_head.setAlignment(Qt.AlignTop)
        HLayout_head.setSpacing(10)
        HLayout_head.addWidget(label_SelectInstrument, 0, Qt.AlignLeft)
        HLayout_head.addWidget(self.comboBox_lyre, 0, Qt.AlignLeft)
        HLayout_head.addWidget(label_MusicalScore, 0, Qt.AlignLeft)
        HLayout_head.addWidget(self.comboBox_head, 0, Qt.AlignLeft)
        HLayout_head.addWidget(button_input, 0, Qt.AlignLeft)
        HLayout_head.addStretch(1)
        HLayout_head.addWidget(button_delete, 0, Qt.AlignRight)
        HLayout_head.addWidget(button_empty, 0, Qt.AlignRight)

        HLayout_end = QHBoxLayout()
        HLayout_end.setSpacing(10)

        HLayout_end.addWidget(label_pADD)
        HLayout_end.addWidget(self.comboBox_pADD)
        HLayout_end.addWidget(label_BufTime)
        HLayout_end.addWidget(self.spinBox_bufTime)
        HLayout_end.addStretch(1)
        HLayout_end.addWidget(self.button_begin, 0, Qt.AlignRight)
        HLayout_end.addWidget(self.button_pauseResume, 0, Qt.AlignRight)
        HLayout_end.addWidget(self.button_cease, 0, Qt.AlignRight)

        # 设置头部组件
        titleLayout = QVBoxLayout()
        titleLayout.addLayout(HLayout_head)
        titleLayout.addLayout(HLayout_key)
        titleLayout.addLayout(HLayout_end)
        # 将头部组件添加到总布局
        self.vBoxLayout.addLayout(titleLayout)
        # 添加组件到总组件
        self.vBoxLayout.addWidget(self.radioWidget, 1, Qt.AlignTop)
        # 执行初始配置
        self.init()

    def init(self):
        """
        读取位置文件并执行方法
        :return:
        """
        # 设置快捷键（开始， 暂停，停止）
        self.setKey()
        # 添加音乐
        songList = ConfigUtil.rYaml("autoPlay", "songList")
        if type(songList) is list:
            for i, j in songList:
                self.addList(False, [i], j)

    def on_press(self, key):
        """
        相应快捷键
        :param key:
        :return:
        """
        if self.QKey[0] in str(key):
            self.button_begin.click()
        elif self.QKey[1] in str(key):
            self.button_pauseResume.click()
        elif self.QKey[2] in str(key):
            self.button_cease.click()

    def setKey(self):
        """
        从配置文件设置快捷键并修改按键文本
        :return:
        """
        begin = ConfigUtil.rYaml("autoPlay", "key", "begin")
        pauseResume = ConfigUtil.rYaml("autoPlay", "key", "pauseResume")
        cease = ConfigUtil.rYaml("autoPlay", "key", "cease")
        # 设置快捷键
        self.QKey = [begin.lower(), pauseResume.lower(), cease.lower()]
        self.button_begin.setText(self.tr('Begin') + " (" + begin + ")")
        self.button_pauseResume.setText(self.tr('Pause/Resume') + " (" + pauseResume + ")")
        self.button_cease.setText(self.tr('Cease') + " (" + cease + ")")
        # 设置下拉框
        self.comboBox_begin.setCurrentIndex(self.key.index(begin))
        self.comboBox_pause_resume.setCurrentIndex(self.key.index(pauseResume))
        self.comboBox_cease.setCurrentIndex(self.key.index(cease))

    def updateKey(self, key, index):
        """
        修改快捷键
        :param key: 快捷键
        :param index: 设置的快捷键索引
        :return:
        """
        key01 = ConfigUtil.rYaml("autoPlay", "key", "begin")
        key02 = ConfigUtil.rYaml("autoPlay", "key", "pauseResume")
        key03 = ConfigUtil.rYaml("autoPlay", "key", "cease")
        if index == 1:
            ConfigUtil.wYaml(key, "autoPlay", "key", "begin")
            if key == key02:
                ConfigUtil.wYaml("None", "autoPlay", "key", "pauseResume")
            if key == key03:
                ConfigUtil.wYaml("None", "autoPlay", "key", "cease")
        elif index == 2:
            ConfigUtil.wYaml(key, "autoPlay", "key", "pauseResume")
            if key == key01:
                ConfigUtil.wYaml("None", "autoPlay", "key", "begin")
            if key == key03:
                ConfigUtil.wYaml("None", "autoPlay", "key", "cease")
        elif index == 3:
            ConfigUtil.wYaml(key, "autoPlay", "key", "cease")
            if key == key01:
                ConfigUtil.wYaml("None", "autoPlay", "key", "begin")
            if key == key02:
                ConfigUtil.wYaml("None", "autoPlay", "key", "pauseResume")
        self.setKey()

    def setScoreType(self):
        """修改琴谱类型"""
        self.scoreType = self.comboBox_head.currentIndex() + 1

    def setLyre(self):
        """修改琴类型"""
        self.lyre = self.comboBox_lyre.currentIndex() + 1

    def setPaDD(self):
        """设置拍提速"""
        self.pADD = self.comboBox_pADD.currentIndex()

    def setBufTime(self):
        """设置缓冲时间"""
        self.bufTime = self.spinBox_bufTime.value()

    def addList(self, box=True, songList=None, scoreType=None):
        """
        添加音乐
        """
        self.songListLength = len(self.songList)
        if box:
            scoreType = self.scoreType
            newList = self.choiceFile()
        else:
            newList = songList
        true = False  # 是否有导入成功
        false = False  # 是否有导入失败
        for i in newList:
            if [i, scoreType] in self.songList:
                false = True
            elif i[-3:] == "mid":
                self.songList.append([i, 0])
                true = True
            elif scoreType == 1:
                if MusicScore.isKe(i)[0]:
                    self.songList.append([i, 1])
                    true = True
                else:
                    false = True
            elif scoreType == 2:
                if MusicScore.isGua(i)[0]:
                    self.songList.append([i, 2])
                    true = True
                else:
                    false = True
            elif scoreType == 3:
                if MusicScore.isYi(i)[0]:
                    self.songList.append([i, 3])
                    true = True
                else:
                    false = True
        if false and box:
            if true:
                self.showMessageDialog("Partial import succeeded")
            else:
                self.showMessageDialog("Import failed")
        self.radioButtonUpdate()  # 更新列表

    def deleteSong(self):
        """
        删除选中的曲
        :return:
        """
        self.songListLength = len(self.songList)
        tmp = 0 - self.buttonGroup.checkedId() - 2
        if tmp == -1:
            self.showMessageDialog("No element selected")
            return
        self.songList.pop(tmp)
        self.radioButtonUpdate()

    def clearSong(self):
        """
        清空所有曲
        """
        self.songListLength = len(self.songList)
        if self.showMessageDialog("Are you sure?"):
            self.songList.clear()
            self.radioButtonUpdate()

    def radioButtonUpdate(self):
        """
        将radioButton更新为列表中的内容
        :return:
        """
        # 同步配置文件
        ConfigUtil.wYaml(self.songList, "autoPlay", "songList")
        # 清除radioButton
        try:
            for i in range(self.songListLength):
                self.radioLayout.removeWidget(self.buttonGroup.button(-2 - i))
        except Exception:
            pass
        self.buttonGroup = QButtonGroup(self.radioWidget)
        # # 增加单选框
        for i in self.songList:
            radioButton = RadioButton(PlayUtil.getName(i[0]), self.radioWidget)
            self.buttonGroup.addButton(radioButton)
            self.radioLayout.addWidget(radioButton)
        self.radioWidget.update()

    def start(self):
        """
        开始演奏
        """
        tmp_order = 0 - self.buttonGroup.checkedId() - 2
        if tmp_order == -1:
            return
        self.playMusic.start(self.songList[tmp_order][0], self.songList[tmp_order][1], self.lyre,
                             self.bufTime, self.pADD)

    def myLabel(self, text):
        """
        创建label
        :param text:
        :return:
        """
        label = QLabel(self.tr(text))
        label.setObjectName('sourcePathLabel')  # 风格设置
        return label

    def choiceFile(self):
        """
        文件选择对话框
        :param self: 父窗口对象
        """
        url = ConfigUtil.rYaml("autoPlay", "fileUrl")
        if url is None or not path.isdir(url):
            key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
            url = QueryValueEx(key, "Desktop")[0]
        flies = QFileDialog.getOpenFileNames(self, self.tr("Choice music score"),
                                             url, self.tr("Music score ") + "(*.txt)")[0]
        if len(flies) > 0:
            ConfigUtil.wYaml(flies[0][:flies[0].rfind("/")], "autoPlay", "fileUrl")
        return flies

    def showMessageDialog(self, text):
        """
        显示消息对话框
        :param text:
        :return:点击确定返回True，否则返回False
        """
        title = self.tr("Message prompt")
        content = self.tr(text)
        w = MessageBox(title, content, self.window())
        if w.exec():
            return True
        else:
            return False
