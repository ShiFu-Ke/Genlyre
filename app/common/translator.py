# coding: utf-8
from PyQt5.QtCore import QObject


class Translator(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.basicInput = self.tr('Basic input')
        self.menus = self.tr('Menus')
        self.dialogs = self.tr('Dialogs')
        self.material = self.tr('Material')
        self.statusInfo = self.tr('Status & info')
        self.scroll = self.tr('Scrolling')
        self.layout = self.tr('Layout')
        self.autoPlay = self.tr('Auto play')
        self.autoPlayTitle = self.tr('After importing the score, it can be played automatically.')
        self.ScoreConversion = self.tr('Music score conversion')
        self.ScoreConversionTitle = self.tr('You can convert the music score to the desired format from here.')
