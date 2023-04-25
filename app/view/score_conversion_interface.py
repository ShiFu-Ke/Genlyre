from os import path
from winreg import OpenKey, HKEY_CURRENT_USER, QueryValueEx

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QFileDialog

from Lib.MusicScore import MusicScore
from qfluentwidgets import (PushButton, PrimaryPushButton, ComboBox, LineEdit, InfoBar, InfoBarPosition)
from util.ConfigUtil import ConfigUtil
from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class ScoreConversionInterface(GalleryInterface):

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.ScoreConversion,
            subtitle=t.ScoreConversionTitle,
            parent=parent
        )
        # 局部变量
        self.inputFile = ""
        self.outputDir = ""
        # mid文件转换类型
        self.arrMid = [self.tr("Mid to script"), self.tr("Mid to integration"), self.tr("Mid to JS")]
        # txt文件转换类型
        self.arrText = [self.tr("Keyboard to number"), self.tr("Number to keyboard"),
                        self.tr("Script to JS"),
                        self.tr("Windsong to vintage(keyboard)")]
        self.conFileType = 0  # 0:未选中；1：mid；2：txt

        # 导入
        # 文本
        label_input = self.myLabel("Input music score：")
        # 文本框
        self.lineEdit_input = LineEdit(self)
        self.lineEdit_input.setReadOnly(True)
        # 按钮
        button_input = PushButton(self.tr('Choice'))
        button_input.clicked.connect(lambda: self.choiceFile())
        # 水平布局
        HLayout_input = QHBoxLayout()
        HLayout_input.setSpacing(10)
        HLayout_input.addWidget(label_input)
        HLayout_input.addWidget(self.lineEdit_input, 1)
        HLayout_input.addWidget(button_input)

        # 导出
        # 文本
        label_output = self.myLabel("Output music directory：")
        # 文本框
        self.lineEdit_output = LineEdit(self)
        self.lineEdit_output.setReadOnly(True)
        # 按钮
        button_output = PushButton(self.tr('Choice'))
        button_output.clicked.connect(lambda: self.choiceDir())
        # 水平布局
        HLayout_output = QHBoxLayout()
        HLayout_output.setSpacing(10)
        HLayout_output.addWidget(label_output)
        HLayout_output.addWidget(self.lineEdit_output, 1)
        HLayout_output.addWidget(button_output)

        # 转换操作
        label_con = self.myLabel("Conversion type:")
        # 下拉框
        self.comboBox_con = ComboBox()
        self.comboBox_con.setCurrentIndex(0)
        self.comboBox_con.setMinimumWidth(260)
        # self.comboBox_con.currentIndexChanged.connect(lambda: print(6))
        # 按钮
        self.button_con = PrimaryPushButton(self.tr('Conversion'))
        self.button_con.setMinimumWidth(80)
        self.button_con.clicked.connect(lambda: self.conversion())
        # 水平布局
        HLayout_con = QHBoxLayout()
        HLayout_con.setSpacing(10)
        HLayout_con.addWidget(label_con)
        HLayout_con.addWidget(self.comboBox_con)
        HLayout_con.addWidget(self.button_con)
        HLayout_con.addStretch(1)

        # 添加水平布局
        self.vBoxLayout.addLayout(HLayout_input)
        self.vBoxLayout.addLayout(HLayout_output)
        self.vBoxLayout.addLayout(HLayout_con)
        # self.vBoxLayout.addWidget(DatePicker(self))

        self.init()

    def init(self):
        """开始调用"""
        tmp = ConfigUtil.rYaml("scoreConversion", "fileUrl")
        if tmp is not None and path.isfile(tmp):
            self.inputFile = tmp
            self.lineEdit_input.setText(tmp)
            self.setComoBoxCon(tmp)
        tmp = ConfigUtil.rYaml("scoreConversion", "dirUrl")
        if tmp is not None and path.isdir(tmp):
            self.outputDir = tmp
            self.lineEdit_output.setText(tmp)
        self.setComoBoxCon(".txt")

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
        url = ConfigUtil.rYaml("scoreConversion", "fileUrl")
        if url is None or not path.isdir(url):
            key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
            url = QueryValueEx(key, "Desktop")[0]
        fileUrl = QFileDialog.getOpenFileName(self, self.tr("Choice music score"), url,
                                              self.tr("Music score ") + "(*.txt)")[0]
        if len(fileUrl) > 0:
            self.inputFile = fileUrl
            self.lineEdit_input.setText(fileUrl)
            ConfigUtil.wYaml(fileUrl, "scoreConversion", "fileUrl")

    def choiceDir(self):
        """路径选择对话框"""
        url = ConfigUtil.rYaml("scoreConversion", "dirUrl")
        if url is None or not path.isdir(url):
            key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
            url = QueryValueEx(key, "Desktop")[0]
        Dir = QFileDialog.getExistingDirectory(self, self.tr("Choice dir"), url)
        if len(Dir.replace(" ", "")) > 0:
            self.outputDir = Dir
            self.lineEdit_output.setText(Dir)
            ConfigUtil.wYaml(Dir, "scoreConversion", "dirUrl")

    def setComoBoxCon(self, fileUrl):
        """设置下拉框内容"""
        self.comboBox_con.clear()
        if fileUrl[-3:] == "mid":
            self.comboBox_con.addItems(self.arrMid)
            self.conFileType = 1
        else:
            self.comboBox_con.addItems(self.arrText)
            self.conFileType = 2
        self.comboBox_con.setCurrentIndex(0)

    def conversion(self):
        if self.conFileType == 0 or not path.isfile(self.inputFile):
            self.boxError(self.tr("Please input a file"))
            return
        if not path.isdir(self.outputDir):
            self.boxError(self.tr("Please select a output path"))
            return
        try:
            if self.conFileType == 1:
                if self.comboBox_con.currentIndex() == 0:
                    MusicScore.midToScript(self.inputFile, self.outputDir)
                elif self.comboBox_con.currentIndex() == 1:
                    MusicScore.midToIntegration(self.inputFile, self.outputDir)
                else:
                    MusicScore.midToJs(self.inputFile, self.outputDir)
            elif self.conFileType == 2:
                if self.comboBox_con.currentIndex() == 0:
                    MusicScore.keyToNumber(self.inputFile, self.outputDir)
                elif self.comboBox_con.currentIndex() == 1:
                    MusicScore.numberToKey(self.inputFile, self.outputDir)
                elif self.comboBox_con.currentIndex() == 2:
                    MusicScore.scriptToJS(self.inputFile, self.outputDir)
                elif self.comboBox_con.currentIndex() == 3:
                    MusicScore.WindsongToVintage(self.inputFile, self.outputDir)
            self.boxSuccess(self.inputFile[self.inputFile.rfind("/") + 1:-4])
        except Exception as e:
            print(e)
            self.boxError(self.inputFile[self.inputFile.rfind("/") + 1:-4])

    def boxSuccess(self, text):
        InfoBar.success(
            title=self.tr('Conversion successful'),
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=2000,  # won't disappear automatically
            parent=self
        )

    def boxError(self, text):
        InfoBar.error(
            title=self.tr('Conversion failed'),
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=2000,  # won't disappear automatically
            parent=self
        )
