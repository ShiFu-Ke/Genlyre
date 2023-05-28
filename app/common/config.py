# coding:utf-8
from enum import Enum

from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, EnumSerializer, FolderValidator)


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = "zh"
    CHINESE_TRADITIONAL = "hk"
    ENGLISH = "en"
    AUTO = "Auto"


class Config(QConfig):
    """ Config of application """

    # folders
    musicFolders = ConfigItem(
        "Folders", "LocalMusic", [], FolderListValidator())
    downloadFolder = ConfigItem(
        "Folders", "Download", "app/download", FolderValidator())

    # main window
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), EnumSerializer(Language), restart=True)

    # Material
    blurRadius = RangeConfigItem("Material", "AcrylicBlurRadius", 15, RangeValidator(0, 40))

    # software update
    checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())


YEAR = 2023
AUTHOR = "keshifu"
VERSION = "v1.0.0"
HOME_URL = "https://space.bilibili.com/660801861"  # up主页
HELP_URL = "https://b23.tv/GnTA6Y5"  # 帮助
DOWNLOAD_URL = "https://keshifu.lanzouk.com/b03vbisqd"  # 下载链接
FEEDBACK_URL = "https://f.wps.cn/g/8neqcjae/"  # 反馈的链接
RECRUIT_URL = "https://f.wps.cn/g/u3lDO1V2/"  # 招募

cfg = Config()
qconfig.load('app/config/config.json', cfg)
