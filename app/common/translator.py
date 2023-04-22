# coding: utf-8
from PyQt5.QtCore import QObject


class Translator(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.autoPlay = self.tr('Auto play')
        self.autoPlayTitle = self.tr('After importing the score, it can be played automatically.')
        self.ScoreConversion = self.tr('Music score conversion')
        self.ScoreConversionTitle = self.tr('You can convert the music score to the desired format from here.')
        self.writeScores = self.tr("Write music scores")
        self.writeScoresTitle = self.tr("You can conveniently write music scores here.")  # 你可以这里方便的写琴谱。
        self.lyre = self.tr("Lyre")
        self.lyreTitle = self.tr("You can play the piano here.")
        self.keyMapping = self.tr("Keyboard Mapping")
        self.keyMappingTitle = self.tr("You can set keyboard mapping while playing.")
        self.practicePiano = self.tr("Practice the piano")
        self.practicePianoTitle = self.tr("You can practice playing the piano here.")  # 你可以在这里练习弹琴。
