# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/30
# @ Time 21:02
class PlayUtil:
    """弹琴工具类"""

    @staticmethod
    def getName(url):
        """
        从琴谱路径获取曲名
        :param url:琴谱路径
        """
        name = url[url.rfind("/") + 1:-4]
        if name[-6:] == "（脚本琴谱）":
            name = name[:-6]
        return name
