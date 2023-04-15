from os import path
from tkinter.tix import Form
from winreg import OpenKey, HKEY_CURRENT_USER, QueryValueEx

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.uic.properties import QtCore
from pyqt5_plugins.examplebutton import QtWidgets

from Lib.PlayMusic import PlayMusic
from ..common.translator import Translator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QButtonGroup, QHBoxLayout, QLabel, QFrame, QFileDialog
from .gallery_interface import GalleryInterface, ToolBar
from qfluentwidgets import (PushButton, ToolButton, PrimaryPushButton, HyperlinkButton,
                            ComboBox, RadioButton, CheckBox, Slider, SwitchButton, IndicatorPosition, MessageBox)
from Lib.MusicScore import MusicScore
from util.PlayUtil import PlayUtil
from util.ConfigUtil import ConfigUtil
from keyboard import add_hotkey, remove_all_hotkeys


class ScoreConversionInterface(GalleryInterface):

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.ScoreConversion,
            subtitle=t.ScoreConversionTitle,
            parent=parent
        )
        # 局部变量
