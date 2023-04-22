# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/17
# @ Time 23:13
from re import sub
from util.Util import Util
from .midi import Midi

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
    def keToGua(data):
        """
        刻师傅格式转呱呱格式
        :param data: 刻师傅格式内容
        :return: 呱呱格式，呱呱时间参数
        """
        time = float(data[:data.find("\n")])
        data_tmp = data.upper().replace("\n", "").replace("L", " ")
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
                    if i[j] in key or i[j] == " ":
                        arr_tmp.append(i[j])
                    elif i[j] == "(":
                        tmp_bracket = True
            length_max = Util.lcm(length_max, len(arr_tmp))
            arr_data.append(arr_tmp.copy())
        arr.clear()
        for i in arr_data:
            tmp = ""
            num = length_max / len(i)  # 每个单元后面的等号个数
            for j in i:
                tmp += j.replace(" ", "") + "=" * int(num)
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
        data_end = str(int((time * 1000) / length_max) / 2) + "\n" + data_end
        return data_end

    @staticmethod
    def yiToGua(data):
        """
        伊蕾娜格式转呱呱格式
        :param data: 伊蕾娜格式内容
        :return: 呱呱格式，呱呱时间参数
        """
        time = int(data[:data.find("\n")])
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
        data_end = str(time) + "\n" + data_end
        return data_end

    @staticmethod
    def guaToke(data):
        """
        呱呱格式转刻师傅格式
        :param data: 呱呱格式内容
        :return: 刻师傅格式
        """
        time = int(data[:data.find("\n")])
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
        data_end = str(((time * 4) / 1000) * 2) + "\n" + data_end
        return data_end

    @staticmethod
    def guaToYi(data):
        """
        呱呱格式转伊蕾娜格式
        :param data: 呱呱格式内容
        :return: 伊蕾娜格式，伊蕾娜时间参数
        """
        time = int(data[:data.find("\n")])
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
                if tmp:
                    pass
                elif i < len(data_tmp) - 1:
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
        if data_end.rfind("(") > data_end.rfind(")"):
            data_end += ")"
        data_end = str(time) + "\n" + data_end
        return data_end

    @staticmethod
    def isKe(filePath):
        """
        刻师傅琴谱格式测试
        :param filePath:琴谱路径
        :return: 格式正确返回True，否则返回False；提示信息
        """
        try:
            file = open(filePath, encoding='utf-8')
            data = file.read()
            file.close()
        except Exception:
            return False, "文件不存在！"
        try:
            float(data[:data.find("\n")])
            data_tmp = data[:data.find("\n")]
            if "." not in data_tmp:
                return False, "首行必须是小数，整数请加\".0\"（如：1.0）！"
            tmp01 = 0
            for i in MusicScore.nuToJp(data[data.find("\n") + 1:]).upper():
                if i in key:
                    tmp01 = 1
                    break
            if tmp01 == 0:
                return False, "琴谱内容为空！"
            tmp01 = 0
            tmp02 = 0
            hang = 1  # 行位置
            lie = 1  # 列位置
            try:
                for i in data:
                    lie += 1
                    if i == "\n":
                        hang += 1
                        lie = 0
                    if i == "(":
                        tmp01 += 1
                    elif i == ")":
                        tmp01 -= 1
                    elif i == "[":
                        tmp02 += 1
                    elif i == "]":
                        tmp02 -= 1
                    elif i == "/":
                        if tmp01 != 0 or tmp02 != 0:
                            return False, "第" + str(hang) + "行，第" + str(lie) + "列存在不匹配的括号！"
                    if tmp01 not in [0, 1] or tmp02 not in [0, 1]:
                        return False, "第" + str(hang) + "行，第" + str(lie) + "列存在不匹配的括号！"
            except IndexError:
                return False, "存在不匹配的括号！"
            if tmp01 != 0:
                return False, "第" + str(hang) + "行，第" + str(lie) + "列存在不匹配的括号！"
            return True, "文件格式正确！"
        except Exception:
            return False, "首行必须是数字(必须小数，如：1.0)！"

    @staticmethod
    def isGua(filePath):
        """
        呱呱琴谱格式测试
        :param filePath: 琴谱路径
        :return: 格式正确返回True，否则返回False；提示信息
        """
        try:
            file = open(filePath, encoding='utf-8')
            data = file.read()
            file.close()
        except Exception:
            return False, "文件不存在！"
        try:
            int(data[:data.find("\n")])
        except Exception:
            return False, "首行必须是数字！"
        for i in data.upper():
            if i in key:
                return True, "格式正确！"
        return False, "琴谱内容为空！"

    @staticmethod
    def isYi(filePath):
        """
        伊蕾娜琴谱格式测试
        :param filePath: 琴谱路径
        :return: 格式正确返回True，否则返回False；提示信息
        """
        try:
            file = open(filePath, encoding='utf-8')
            data = file.read()
            file.close()
        except Exception:
            return False, "文件不存在！"
        try:
            int(data[:data.find("\n")])
        except Exception:
            return False, "首行必须是数字！"
        for i in data.upper():
            if i in key:
                return True, "格式正确！"
        return False, "琴谱内容为空！"

    @staticmethod
    def formatKe(data):
        """
        格式换刻师傅琴谱，将以前的空音用空格代替
        判断传入数据书否存在L，如果存在，则L表示空音，转为空格
        :param data:格式化前
        :return:格式化后
        """
        if data.count("L") > 0:
            return data.replace(" ", "").replace("L", " ")
        return data

    @staticmethod
    def fwToLj(data):
        """
        风物之诗琴谱转老旧的诗琴谱
        :param data: 琴谱按键
        :return: 转换后按键
        """
        data01 = "ZXCVBNMASDFGHJQWERTYU"
        data02 = "AZXCVBNMASDFGHJQSERTH"
        out = ""
        for j in data:
            if j in data01:
                out += data02[data01.find(j)]
            else:
                out += j
        out = sub("MM", "M", out)
        out = sub("SS", "S", out)
        out = sub("HH", "H", out)
        return out

    @staticmethod
    def nuToJp(number):
        """
        数字转键盘
        :param number: 数字格式的琴谱
        :return: 键盘格式的琴谱
        """
        # 加第一行数字
        data = number.split("\n")[0] + "\n"
        number = number[number.find("\n") + 1:]
        key_up = 'QWERTYU'
        key_mid = 'ASDFGHJ'
        key_down = 'ZXCVBNM'
        i = 0
        length = len(number)
        while i < length:
            try:
                if 1 <= int(number[i]) <= 7:
                    data += key_mid[int(number[i]) - 1]
                    i += 1
                    continue
            except ValueError:
                pass
            if number[i] == '+' and number[i + 1].isalnum():
                data += key_up[int(number[i + 1]) - 1]
                i += 2
                continue
            if number[i] == '-' and number[i + 1].isalnum():
                data += key_down[int(number[i + 1]) - 1]
                i += 2
                continue
            if number[i] == '0':
                data += "L"
                i += 1
                continue
            data += number[i]
            i += 1
        return data

    @staticmethod
    def WindsongToVintage(url, output):
        """风物之诗琴谱转老旧的诗琴谱"""
        file = open(url, 'r', encoding="UTF-8")
        data = file.read()
        file.close()
        data01 = "ZXCVBNMASDFGHJQWERTYU"
        data02 = "AZXCVBNMASDFGHJQSERTH"
        out = ""
        for j in data:
            if j in data01:
                out += data02[data01.find(j)]
            else:
                out += j
        out = sub("MM", "M", out)
        out = sub("SS", "S", out)
        out = sub("HH", "H", out)
        file01 = open(output + url[url.rfind("/"):-4] + "(老旧).txt", 'w', encoding="UTF-8")
        file01.write(out)
        file01.close()

    @staticmethod
    def numberToKey(url, output):
        """数字转键盘"""
        # 加第一行数字
        file = open(url, 'r', encoding="UTF-8")
        number = file.read()
        file.close()
        key_up = 'QWERTYU'
        key_mid = 'ASDFGHJ'
        key_down = 'ZXCVBNM'
        data = ""
        i = 0
        length = len(number)
        while i < length:
            try:
                if 1 <= int(number[i]) <= 7:
                    data += key_mid[int(number[i]) - 1]
                    i += 1
                    continue
            except ValueError:
                pass
            if number[i] == '+' and number[i + 1].isalnum():
                data += key_up[int(number[i + 1]) - 1]
                i += 2
                continue
            if number[i] == '-' and number[i + 1].isalnum():
                data += key_down[int(number[i + 1]) - 1]
                i += 2
                continue
            if number[i] == '0':
                data += "L"
                i += 1
                continue
            data += number[i]
            i += 1
        file01 = open(output + url[url.rfind("/"):-4] + "(键盘).txt", 'w', encoding="UTF-8")
        file01.write(data)
        file01.close()

    @staticmethod
    def keyToNumber(url, output):
        """键盘转数字"""
        key_up = 'QWERTYU'
        key_mid = 'ASDFGHJ'
        key_down = 'ZXCVBNM'
        file = open(url, 'r', encoding="UTF-8")
        tmp = file.read()
        file.close()
        data = ""
        for i in tmp:
            if i.upper() in key_up:
                data += "+" + str(key_up.index(i.upper()) + 1)
            elif i.upper() in key_mid:
                data += str(key_mid.index(i.upper()) + 1)
            elif i.upper() in key_down:
                data += "-" + str(key_down.index(i.upper()) + 1)
            elif i.upper() == "L":
                data += " "
            else:
                data += i
        file01 = open(output + url[url.rfind("/"):-4] + "(数字).txt", 'w', encoding="UTF-8")
        file01.write(data)
        file01.close()

    @staticmethod
    def scriptToJS(url, output):
        """脚本转js"""
        file = open(url, 'r', encoding="UTF-8")
        tmp = file.read()
        file.close()
        tmp = MusicScore.keToGua(tmp)
        MusicScore.guaToJS(tmp[tmp.find("\n"):], float(tmp[:tmp.find("\n")]), url, output)

    @staticmethod
    def midToJs(url, output):
        data = Midi.get_keys(url)
        MusicScore.guaToJS(data[0], data[2], url, output)

    @staticmethod
    def guaToJS(data, time, url, output):
        dataKey = data.replace("\n", "").replace("+", "====").replace("-", "==")
        dataEnd = Midi.jsTitle + "\n"
        if len(dataKey) > 0:
            while dataKey[0] == "=":
                dataKey = dataKey[1:]
        time = time
        tmp = 0
        for i in dataKey:
            if i == "=":
                tmp += 1
            else:
                if tmp > 0:
                    dataEnd += "t(" + str(int(tmp * time)) + ");\n"
                    tmp = 0
                dataEnd += i + "();\n"
        file02 = open(output + url[url.rfind("/"):-4] + ".js", 'w', encoding="UTF-8")
        file02.write(dataEnd)
        file02.close()

    @staticmethod
    def midToScript(url, output):
        """midi转脚本"""
        data = Midi.get_keys(url)

        keData = MusicScore.guaTokeSou(data[0])  # 刻师傅格式，不带时间
        # 导出刻师傅脚本琴谱
        file01 = open(output + url[url.rfind("/"):-4] + "（脚本琴谱）.txt", 'w', encoding="UTF-8")
        file01.write(str(data[1]) + "\n" + keData)
        file01.close()

    @staticmethod
    def midToIntegration(url, output):
        """mid转整合"""
        data = Midi.get_keys(url)
        keData = MusicScore.guaTokeSou(data[0])  # 刻师傅格式，不带时间
        # 导出刻师傅整合琴谱
        file01 = open(output + url[url.rfind("/"):-4] + "(整合琴谱).txt", 'w', encoding="UTF-8")
        file01.write(MusicScore.transition(keData))
        file01.close()

    @staticmethod
    def midToGua(url, output):
        """mid转呱"""
        data = Midi.get_keys(url)
        # 导出呱格式
        file02 = open(output + url[url.rfind("/"):-4] + "(呱).txt", 'w', encoding="UTF-8")
        file02.write(str(int(data[1] * 125)) + "\n" + data[0])
        file02.close()

    @staticmethod
    def transition(InStr):
        """
        键盘转整合
        :param InStr: 键盘
        :return: 整合
        """
        jp = ["Q", "W", "E", "R", "T", "Y", "U", "A", "S", "D", "F", "G", "H", "J", "Z", "X", "C", "V", "B", "N", "M"]
        sz = ["+1", "+2", "+3", "+4", "+5", "+6", "+7", "1", "2", "3", "4", "5", "6", "7", "-1", "-2", "-3", "-4", "-5",
              "-6",
              "-7"]
        dataStr = ""
        for k in InStr:
            if k in jp:
                dataStr += sz[jp.index(k)]
            else:
                dataStr += k
        end = "键盘:\n" + InStr + "\n\n\n数字:\n" + dataStr
        return end

    @staticmethod
    def guaTokeSou(dataGua):
        """
        呱呱格式转刻师傅格式
        :param dataGua: 呱呱格式内容
        :return: 刻师傅格式，刻师傅时间参数
        """
        data_tmp = dataGua.upper().replace(" ", "").replace("\n", "").replace("+", "====").replace("-", "==")
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
        return data_end
