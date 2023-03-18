# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/17
# @ Time 23:13
from Lib.Util import Util

key = ["Z", "X", "C", "V", "B", "N", "M", "A", "S", "D", "F", "G", "H", "J", "Q", "W", "E", "R", "T", "Y", "U"]


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
        data_tmp = data.upper().replace("\n", "")
        data_end = ""
        for i in data_tmp:
            if i in ["/", "(", ")", " "] or i in key:
                data_end += i
        data_tmp = data_end
        arr_tmp = data_tmp.split("/")
        # 将每拍放入数组
        arr = []
        for i in arr_tmp:
            if len(i) > 0:
                arr.append(i)
        arr_data = []
        tmp = ""
        tmp_bracket = False  # 记录是否在括号内
        length_max = 1  # 记录每拍最多音个数
        for i in arr:
            arr_tmp.clear()
            for j in range(len(i)):
                if tmp_bracket:
                    tmp += i[j]
                    if i[j + 1] == ")":
                        tmp_bracket = False
                        arr_tmp.append(tmp)
                        tmp = ""
                else:
                    a = i[j]
                    if i[j] in key or i[j] == " ":
                        arr_tmp.append(i[j])
                    elif i[j] == "(":
                        tmp_bracket = True
            length_max = Util.lcm(length_max, len(arr_tmp))
            arr_data.append(arr_tmp.copy())
        time0 = int((time * 1000) / length_max)
        arr.clear()
        for i in arr_data:
            tmp = ""
            num = length_max / len(i)  # 每个单元后面的等号个数
            for j in i:
                tmp += j + "=" * int(num)
            arr.append(tmp.replace(" ", "").replace("====", "+").replace("==", "-"))
        data_end = ""
        for i in range(len(arr)):
            data_end += arr[i]
            if (i + 1) % 4 == 0:
                data_end += "\n"
        # 处理后面
        data_end += (4 - (len(arr) % 4)) * "+"
        if data_end[-5:] == "\n++++":
            data_end = data_end[:-5]
        return data_end, time0

    @staticmethod
    def yiToGua(data, time):
        """
        伊蕾娜格式转呱呱格式
        :param data: 伊蕾娜格式内容
        :param time: 伊蕾娜参数
        :return: 呱呱格式，呱呱时间参数
        """

        data_init = data.upper().replace("\n", "")
        data_end = ""
        for i in data_init:
            if i in ["=", "(", ")", " "] or i in key:
                data_end += i
        data_init = data_end
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
        if data_end[-5:] == "\n++++":
            data_end = data_end[:-5]
        return data_end, time

    @staticmethod
    def GuaToke(data, time):
        """
        呱呱格式转刻师傅格式
        :param data: 呱呱格式内容
        :param time: 呱呱时间参数
        :return: 刻师傅格式，刻师傅时间参数
        """
        data_tmp = data.upper().replace(" ", "").replace("\n", "").replace("+", "====").replace("-", "==")
        data_end = ""
        for i in data_tmp:
            if i == "=" or i in key:
                data_end += i
        data_tmp = data_end
        # 去掉前面和后面的=
        while data_tmp[-1] == "=":
            data_tmp = data_tmp[:-1]
        while data_tmp[0] == "=":
            data_tmp = data_tmp[1:]
        # 补充后面=
        data_tmp += (4 - (data_tmp.count("=") % 4)) * "="
        arr = []
        tmp_num = 0
        tmp_str = ""
        for i in data_tmp:
            tmp_str += i
            if i == "=":
                tmp_num += 1
            if tmp_num == 4:
                arr.append(tmp_str)
                tmp_str = ""
                tmp_num = 0
        tmp_bracket = False  # 记录是否在括号内
        for i in range(len(arr)):
            tmp = ""
            for j in range(len(arr[i])):
                if arr[i][j] == "=":
                    if j == 0:
                        tmp += " "
                    elif arr[i][j - 1] == "=":
                        tmp += " "
                    elif arr[i][j - 1] in key:
                        pass
                elif arr[i][j] in key:
                    if tmp_bracket:
                        tmp += arr[i][j]
                        if arr[i][j + 1] == "=":
                            tmp += ")"
                            tmp_bracket = False
                    elif arr[i][j + 1] in key:
                        tmp += "(" + arr[i][j]
                        tmp_bracket = True
                    else:
                        tmp += arr[i][j]
            arr[i] = tmp + "/"
        data_end = ""
        for i in range(len(arr)):
            data_end += arr[i]
            if (i + 1) % 4 == 0:
                data_end += "\n"
        # 后面处理
        data_end += "    /" * (4 - (len(arr) % 4))
        if data_end[-21:] == "\n    /    /    /    /":
            data_end = data_end[:-21]
        return data_end, (time * 4) / 1000

    @staticmethod
    def GuaToYi(data, time):
        """
        呱呱格式转伊蕾娜格式
        :param data: 呱呱格式内容
        :param time: 呱呱时间参数
        :return: 伊蕾娜格式，伊蕾娜时间参数
        """
        data_tmp = data.replace("+", "====").replace("-", "==").replace("\n", "").upper()
        data_end = ""
        for i in data_tmp:
            if i == "=" or i in key:
                data_end += i
        data_tmp = data_end
        # 去掉后面的等号
        while data_tmp[-1] == "=":
            data_tmp = data_tmp[:-1]
        # 去掉前面的等号
        while data_tmp[0] == "=":
            data_tmp = data_tmp[1:]
        data_end = ""
        tmp = False  # 是否在括号内
        for i in range(len(data_tmp)):
            if data_tmp[i] != "=":
                if i < len(data_tmp) - 1:
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

    @staticmethod
    def FormatKe(data):
        """
        格式换刻师傅琴谱，将以前的空音用空格代替
        判断传入数据书否存在L，如果存在，则L表示空音，转为空格
        :param data:格式化前
        :return:格式化后
        """
        if data.count("L") > 0:
            return data.replace(" ", "").replace("L", " ")
        return data
