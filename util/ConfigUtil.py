# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/29
# @ Time 20:12
import yaml


class ConfigUtil:
    """
    配置文件操作
    """

    @staticmethod
    def rYaml(key01=None, key02=None, key03=None):
        """
        读取配置文件
        :param key01: 一级key，可以为空
        :param key02: 二级key，可以为空
        :param key03: 三级key，可以为空
        :return: 键值对或对应的值
        """
        try:
            file = open("..\\config.yaml", "r", encoding="utf-8")
            data = yaml.load(file.read())
            file.close()
        except Exception:
            return None
        if key01 is None:
            return data
        if key02 is None:
            return data.get(key01)
        if key03 is None:
            return data.get(key01).get(key02)
        else:
            return data.get(key01).get(key02).get(key03)

    @staticmethod
    def wYaml(data, key01=None, key02=None, key03=None):
        """
        写配置文件
        :param data: 要写的内容
        :param key01: 一级key，可以为空
        :param key02: 二级key，可以为空
        :param key03: 三级key，可以为空
        :return:
        """
        tmp = ConfigUtil.rYaml()
        if key01 is None:
            tmp = data
        elif key02 is None:
            tmp[key01] = data
        elif key03 is None:
            tmp[key01][key02] = data
        else:
            tmp[key01][key02][key03] = data
        with open("..\\config.yaml", "w", encoding="utf-8") as f:
            yaml.dump(tmp, f)
        print(tmp)


print(ConfigUtil.rYaml("a"))
ConfigUtil.wYaml({"a": 1, "b": [1, 2, 3]})
