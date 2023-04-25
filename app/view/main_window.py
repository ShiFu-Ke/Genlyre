# coding: utf-8
from os import system

from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget
from qframelesswindow import FramelessWindow

from Lib.PlaySound import PlaySound
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, MessageBox,
                            isDarkTheme, PopUpAniStackedWidget)
from util import Util
from .autoPlay_interface import AutoPlayInterface
from .gallery_interface import GalleryInterface
from .home_interface import HomeInterface
from .keyMapping_interface import KeyMappingInterface
from .lyre_interface import LyreInterface
from .practice_piano_interface import PracticePianoInterface
from .score_conversion_interface import ScoreConversionInterface
from .setting_interface import SettingInterface, cfg
from .title_bar import CustomTitleBar
from .write_scores_interface import WriteScoresInterface
from ..common.icon import Icon
from ..common.signal_bus import signalBus


class StackedWidget(QFrame):
    """ Stacked widget """

    currentWidgetChanged = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)
        playSound = PlaySound()
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(
            lambda i: self.currentWidgetChanged.emit(self.view.widget(i)))

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def setCurrentWidget(self, widget, popOut=False):
        widget.verticalScrollBar().setValue(0)
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.InQuad)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class MainWindow(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        self.widgetLayout = QHBoxLayout()

        self.stackWidget = StackedWidget(self)
        self.navigationInterface = NavigationInterface(self, True, True)

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.settingInterface = SettingInterface(self)
        self.autoPlayInterface = AutoPlayInterface(self)
        self.scoreConversionInterface = ScoreConversionInterface(self)
        self.lyreInterface = LyreInterface(self)
        self.keyMappingInterface = KeyMappingInterface(self)
        self.writeScoresInterface = WriteScoresInterface(self)
        self.practicePianoInterface = PracticePianoInterface(self)

        self.stackWidget.addWidget(self.homeInterface)
        self.stackWidget.addWidget(self.settingInterface)
        self.stackWidget.addWidget(self.autoPlayInterface)
        self.stackWidget.addWidget(self.scoreConversionInterface)
        self.stackWidget.addWidget(self.lyreInterface)
        self.stackWidget.addWidget(self.keyMappingInterface)
        self.stackWidget.addWidget(self.writeScoresInterface)
        self.stackWidget.addWidget(self.practicePianoInterface)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def closeEvent(self, event):
        """重写关闭窗口的方法"""
        Util.cmd("TASKKILL /IM KeyboardMapping.exe /F")
        super().closeEvent(event)

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addLayout(self.widgetLayout)
        self.hBoxLayout.setStretchFactor(self.widgetLayout, 1)

        self.widgetLayout.addWidget(self.stackWidget)
        self.widgetLayout.setContentsMargins(0, 48, 0, 0)

        signalBus.switchToSampleCard.connect(self.switchToSample)

        self.navigationInterface.displayModeChanged.connect(
            self.titleBar.raise_)
        self.titleBar.raise_()

    def initNavigation(self):
        self.homeInterface.setObjectName('homeInterface')
        self.autoPlayInterface.setObjectName('autoPlayInterface')
        self.scoreConversionInterface.setObjectName("scoreConversionInterface")
        self.lyreInterface.setObjectName("lyreInterface")
        self.keyMappingInterface.setObjectName("keyMappingInterface")
        self.writeScoresInterface.setObjectName("writeScoresInterface")
        self.practicePianoInterface.setObjectName("practicePianoInterface")
        self.settingInterface.setObjectName('settingsInterface')

        # add navigation items
        self.navigationInterface.addItem(
            routeKey=self.homeInterface.objectName(),
            icon=Icon.HOME,
            text=self.tr('Home'),
            onClick=lambda t: self.switchTo(self.homeInterface, t)
        )
        self.navigationInterface.addSeparator()

        self.navigationInterface.addItem(
            routeKey=self.autoPlayInterface.objectName(),
            icon=Icon.AUTO,
            text=self.tr('Auto play'),  # 菜单文本标题
            onClick=lambda t: self.switchTo(self.autoPlayInterface, t),
            position=NavigationItemPosition.SCROLL
        )

        self.navigationInterface.addItem(
            routeKey=self.scoreConversionInterface.objectName(),
            icon=Icon.CONVERSION,
            text=self.tr('Music score conversion'),  # 菜单文本标题
            onClick=lambda t: self.switchTo(self.scoreConversionInterface, t),
            position=NavigationItemPosition.SCROLL
        )

        self.navigationInterface.addItem(
            routeKey=self.writeScoresInterface.objectName(),
            icon=Icon.MUSICSCORE,
            text=self.tr('Write music scores'),  # 菜单文本标题
            onClick=lambda t: self.switchTo(self.writeScoresInterface, t),
            position=NavigationItemPosition.SCROLL
        )

        self.navigationInterface.addItem(
            routeKey=self.lyreInterface.objectName(),
            icon=Icon.LYRE,
            text=self.tr('Lyre'),  # 菜单文本标题
            onClick=lambda t: self.switchTo(self.lyreInterface, t),
            position=NavigationItemPosition.SCROLL
        )

        self.navigationInterface.addItem(
            routeKey=self.keyMappingInterface.objectName(),
            icon=Icon.KRY,
            text=self.tr('Keyboard Mapping'),  # 菜单文本标题
            onClick=lambda t: self.switchTo(self.keyMappingInterface, t),
            position=NavigationItemPosition.SCROLL
        )

        self.navigationInterface.addItem(
            routeKey=self.practicePianoInterface.objectName(),
            icon=Icon.HELP,
            text=self.tr('Practice the piano'),  # 菜单文本标题
            onClick=lambda t: self.switchTo(self.practicePianoInterface, t),
            position=NavigationItemPosition.SCROLL
        )

        self.navigationInterface.addItem(
            routeKey=self.settingInterface.objectName(),
            icon=FIF.SETTING,
            text='Settings',
            onClick=lambda t: self.switchTo(self.settingInterface, t),
            position=NavigationItemPosition.BOTTOM
        )

        # !IMPORTANT: don't forget to set the default route key if you enable the return button
        self.navigationInterface.setDefaultRouteKey(
            self.homeInterface.objectName())

        self.stackWidget.currentWidgetChanged.connect(
            lambda w: self.navigationInterface.setCurrentItem(w.objectName()))
        self.navigationInterface.setCurrentItem(
            self.homeInterface.objectName())
        self.stackWidget.setCurrentIndex(0)

    def initWindow(self):
        self.resize(1000, 780)
        self.setMinimumWidth(580)
        self.setWindowIcon(QIcon('app/resource/images/logo01.png'))
        self.setWindowTitle('Genlyre')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        cfg.themeChanged.connect(self.setQss)
        self.setQss()

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'app/resource/qss/{color}/main_window.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget, triggerByUser=True):
        self.stackWidget.setCurrentWidget(widget, not triggerByUser)
        widget.setFocus()

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width() - 46, self.titleBar.height())

    def switchToSample(self, routeKey):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackWidget.setCurrentWidget(w)
