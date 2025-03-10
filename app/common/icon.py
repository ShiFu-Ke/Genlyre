# coding: utf-8
from enum import Enum

from qfluentwidgets import FluentIconBase, getIconColor, Theme


class Icon(FluentIconBase, Enum):
    HOME = "Home"
    CHAT = "Chat"
    CODE = "Code"
    MENU = "Menu"
    ALBUM = "Album"
    SCROLL = "Scroll"
    LAYOUT = "Layout"
    GITHUB = "GitHub"
    MESSAGE = "Message"
    CHECKBOX = "CheckBox"
    DOCUMENT = "Document"
    CONSTRACT = "Constract"
    BLIBLI = "blibli"
    LYRE = "lyre"
    AUTO = "auto"
    CONVERSION = "conversion"
    KRY = "key"
    MUSICSCORE = "musicScore"
    HELP = "help"
    HELP01 = "help01"
    DOWNLOAD = "download"

    def path(self, theme=Theme.AUTO):
        if theme == Theme.AUTO:
            c = getIconColor()
        else:
            c = "white" if theme == Theme.DARK else "black"

        return f"app/resource/images/icons/{self.value}_{c}.svg"
