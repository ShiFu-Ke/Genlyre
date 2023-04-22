from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QHBoxLayout, QLabel

from qfluentwidgets import (PushButton)
from .gallery_interface import GalleryInterface
from ..common.config import RECRUIT_URL
from ..common.translator import Translator


class PracticePianoInterface(GalleryInterface):
    key = ["Q", "W", "E", "R", "T", "Y", "U", "A", "S", "D", "F", "G", "H", "J", "Z", "X", "C", "V", "B", "N", "M"]

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.practicePiano,
            subtitle=t.practicePianoTitle,
            parent=parent
        )
        # 局部变量

        # 文本
        label_msg = self.myLabel(
            "If you are interested in this software, if you know python and can write waterfall streams, please sign up for this project. If you want to take part")
        label_msg.setWordWrap(True)
        label_msg.setAlignment(Qt.AlignCenter)
        label_note = self.myLabel(
            "Note: This software is completely free and there is no salary for participating in this program (0.0)")
        label_note.setWordWrap(True)
        label_note.setAlignment(Qt.AlignCenter)
        button = PushButton(self.tr("click here"))
        button.setMaximumWidth(120)
        button.clicked.connect(lambda: self.openURL())

        HLayout_head = QHBoxLayout()
        HLayout_head.setSpacing(0)
        HLayout_head.addStretch(1)
        HLayout_head.addWidget(label_msg, 4)
        HLayout_head.addStretch(1)

        HLayout_button = QHBoxLayout()
        HLayout_button.setSpacing(0)
        HLayout_button.addStretch(1)
        HLayout_button.addWidget(button, 4)
        HLayout_button.addStretch(1)

        HLayout_note = QHBoxLayout()
        HLayout_note.setSpacing(0)
        HLayout_note.addStretch(1)
        HLayout_note.addWidget(label_note, 4)
        HLayout_note.addStretch(1)

        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addLayout(HLayout_head)
        self.vBoxLayout.addLayout(HLayout_button)
        self.vBoxLayout.addLayout(HLayout_note)
        self.vBoxLayout.addStretch(2)

    @staticmethod
    def openURL():
        QDesktopServices.openUrl(QUrl(RECRUIT_URL))

    def myLabel(self, text):
        """
        创建label
        :param text:
        :return:
        """
        label = QLabel(self.tr(text))
        label.setObjectName('sourcePathLabel')  # 风格设置
        return label
