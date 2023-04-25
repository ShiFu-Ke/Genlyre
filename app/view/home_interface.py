# coding:utf-8

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon
from ..common.config import cfg, HELP_URL, DOWNLOAD_URL, FEEDBACK_URL
from ..common.icon import Icon
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView


class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)
        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel('Genlyre', self)
        self.banner = QPixmap('app/resource/images/header1.png')
        self.linkCardView = LinkCardView(self)

        self.galleryLabel.setObjectName('galleryLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            'app/resource/images/logo02.png',
            self.tr('UP home page'),
            self.tr('Click here to watch the piano playing video.'),
            HELP_URL
        )

        self.linkCardView.addCard(
            Icon.HELP01,
            self.tr('Usage method'),
            self.tr('Click here to view tutorials on how to use each feature.'),
            HELP_URL
        )

        self.linkCardView.addCard(
            Icon.DOWNLOAD,
            self.tr('Download'),
            self.tr('Click to check for updates to the latest version of Genlyre.'),
            DOWNLOAD_URL
        )

        self.linkCardView.addCard(
            FluentIcon.FEEDBACK,
            self.tr('Send feedback'),
            self.tr('Help us improve Genlyre by providing feedback.'),
            FEEDBACK_URL
        )

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), 200
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        # draw background color
        painter.fillPath(path, QColor(206, 216, 228))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), transformMode=Qt.SmoothTransformation)
        path.addRect(QRectF(0, h, w, self.height() - h))
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.__setQss()

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        cfg.themeChanged.connect(self.__setQss)

    def __setQss(self):
        self.view.setObjectName('view')
        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'app/resource/qss/{theme}/home_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def loadSamples(self):
        """ load samples """
        basicInputView = SampleCardView(
            self.tr("Quick jump"), self.view)
        basicInputView.addSampleCard(
            icon="app/resource/images/controls/auto.png",
            title=self.tr("Auto play"),
            content=self.tr(
                "After importing the score, it can be played automatically."),
            routeKey="autoPlayInterface",
        )
        basicInputView.addSampleCard(
            icon="app/resource/images/controls/conversion.png",
            title=self.tr("Music score conversion"),
            content=self.tr(
                "You can convert the music score to the desired format from here."),
            routeKey="scoreConversionInterface",
        )
        basicInputView.addSampleCard(
            icon="app/resource/images/controls/scores.png",
            title=self.tr("Write music scores"),
            content=self.tr(
                "You can conveniently write music scores here."),
            routeKey="writeScoresInterface",
        )
        basicInputView.addSampleCard(
            icon="app/resource/images/controls/lyre.png",
            title=self.tr("Lyre"),
            content=self.tr(
                "You can play the piano here."),
            routeKey="lyreInterface",
        )
        basicInputView.addSampleCard(
            icon="app/resource/images/controls/key.png",
            title=self.tr("Keyboard Mapping"),
            content=self.tr(
                "You can set keyboard mapping while playing."),
            routeKey="keyMappingInterface",
        )
        self.vBoxLayout.addWidget(basicInputView)
