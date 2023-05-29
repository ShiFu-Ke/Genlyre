# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/04/13
# @ Time 18:06
import time
import logging  # logging默认值打印warning以上级别的信息
import traceback  # 将原始报错的信息返回出来


class Log:
    def __init__(self, LogName):
        logging.basicConfig(level='INFO', filename=LogName, filemode='a+')

    @staticmethod
    def addLog():
        error = traceback.format_exc()
        logging.error(time.strftime('%y-%m-%d %H:%M:%S') + "\n" + error + '-------------- \n')
