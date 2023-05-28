# @ Created with PyCharm Professional 2021.2.1
# @ Author KeShiFu
# @ Date 2023/05/26
# @ Time 10:52
import urllib.request

import yaml


class UpDate:
    @staticmethod
    def getUpdateMsg(name):
        """
        在线获取版本号
        :param name: 软件名称
        :return: [版本号，文件名称，下载链接]
        """
        url = 'https://gitee.com/Ke_ShiFu/file/raw/master/update.yaml'
        data = yaml.load(urllib.request.urlopen(url).read())
        file_name = data.get(name).get("name")
        uri = "https://gitee.com/Ke_ShiFu/file/raw/master/" + name + "/" + file_name
        version = data.get(name).get("version")
        return version, file_name, uri

    @staticmethod
    def download(path, url):
        """
        下载软件
        :param path:
        :param url:
        :return:
        """
        try:
            urllib.request.urlretrieve(url, path)
            print("下载成功！")
        except Exception as e:
            print("下载失败！")
            print(e)
