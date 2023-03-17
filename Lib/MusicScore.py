# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/17
# @ Time 23:13

class MusicScore:
    """
    琴谱处理类
    琴谱格式：
        1.刻师傅/指尖格式：括号内为同时按，/是拍子，空格是空音，时间参数为每拍总时间(s),必须小数，演奏是自动分配到每个单元
        2.呱呱格式：加号(+)为一拍，减号(-)为半拍，等号(=)为四分之一拍,时间参数为=的时长(ms)
        3.伊蕾娜格式：空格表示停顿，括号内同时按，时间参数为四分之一拍的时长(ms)
    以呱呱谱为中间格式
    """

    @staticmethod
    def keToGua(data, time):
        """
        刻师傅格式转呱呱格式
        :param data: 刻师傅格式内容
        :param time: 刻师傅时间参数
        :return: 呱呱格式，呱呱时间参数
        """
        pass

    @staticmethod
    def yiToGua(data, time):
        """
        伊蕾娜格式转呱呱格式
        :param data: 伊蕾娜格式内容
        :param time: 伊蕾娜参数
        :return: 呱呱格式，呱呱时间参数
        """

        data_init = data.upper().replace("\n", "")
        data_tmp = ''
        tmp = False  # 记录位置是否在括号内
        # 全部转为等号
        for i in data_init:
            if i == " ":
                data_tmp += "="
            elif i == "(":
                data_tmp += i
                tmp = True
            elif i == ")":
                data_tmp += i + "="
                tmp = False
            elif i.isalpha():
                data_tmp += i
                if not tmp:
                    data_tmp += "="
        data_end = ""
        tmp = 0  # 记录等号个数
        # 每拍换行
        for i in data_tmp:
            data_end += i
            if i == "=":
                tmp += 1
            if tmp == 4:
                data_end += "\n"
                tmp = 0
        # 处理后面
        data_end += (4 - tmp) * "="
        # 换符号
        data_end = data_end.replace("====", "+").replace("==", "-").replace("(", "").replace(")", "")
        # 将4节放一行
        arr = data_end.split("\n")
        data_end = ""
        for i in range(len(arr)):
            data_end += arr[i]
            if (i + 1) % 4 == 0:
                data_end += "\n"
        # 处理后面
        data_end += (4 - (len(arr) % 4)) * "+"
        return data_end, time

    @staticmethod
    def GuaToke(data, time):
        """
        呱呱格式转刻师傅格式
        :param data: 呱呱格式内容
        :param time: 呱呱时间参数
        :return: 刻师傅格式，刻师傅时间参数
        """
        date_tmp = data.upper().replace(" ", "").replace("\n", "")
        data_end = ""
        # 将所有符号变为=
        for i in date_tmp:
            if i == "+":
                data_end += "===="
            elif i == "-":
                data_end += "=="
            elif i == "=":
                data_end += "="
            elif i.encode('UTF-8').isalpha():
                data_end += i
        tmp01 = 0  # 记录每个音
        tmp02 = 0  # 记录每节
        date02 = "("
        for i in range(len(data_end)):
            if data_end[i] == "=":
                if data_end[i - 1].isalpha():
                    date02 += ")"
                tmp01 += 1
                if tmp01 == 4:
                    tmp02 += 1
                    date02 += " /"
                if tmp02 == 4:
                    date02 += "\n"
                try:
                    if data_end[i + 1].isalpha():
                        date02 += "("
                except IndexError:
                    pass
                tmp01 %= 4
                tmp02 %= 4
            else:
                date02 += data_end[i]

        # 去括号后面加斜杠
        data_end = ""
        i = 0
        while i < len(date02):
            try:
                if date02[i] == "(" and date02[i + 2] == ")":
                    data_end += date02[i + 1]
                    i += 3
                else:
                    data_end += date02[i]
                    i += 1
            except IndexError:
                data_end += date02[i]
                i += 1
        if data_end[-1].isalpha():
            data_end += "/" * (4 - tmp02)
        return data_end, 0.6

    @staticmethod
    def GuaToYi(data, time):
        """
        呱呱格式转伊蕾娜格式
        :param data: 呱呱格式内容
        :param time: 呱呱时间参数
        :return: 伊蕾娜格式，伊蕾娜时间参数
        """
        data_tmp = data.replace("+", "====").replace("-", "==").replace("\n", "").upper()
        # 去掉后面的等号
        while data_tmp[-1] == "=":
            data_tmp = data_tmp[:-1]
        data_tmp = data.replace("+", "====").replace("-", "==").replace("\n", "")
        # 去掉前面的等号
        while data_tmp[0] == "=":
            data_tmp = data_tmp[1:]
        data_end = ""
        tmp = False  # 是否在括号内
        for i in range(len(data_tmp)):
            if data_tmp[i] != "=":
                if data_tmp[i + 1] != "=":
                    data_end += "("
                    tmp = True
                data_end += data_tmp[i]
            if data_tmp[i] == "=" and i > 0:
                if data_tmp[i - 1] == "=":
                    data_end += " "
                if tmp:
                    data_end += ")"
                    tmp = False
        return data_end, time
