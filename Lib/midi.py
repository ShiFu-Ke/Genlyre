# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/02/20
# @ Time 20:37
from math import gcd

from mido import MidiFile


class Midi:
    """mid文件的处理"""
    jsTitle = """toast("转谱：原琴玩家刻师傅");
    sleep(200);
    var speedControl=1;
    var s=1;
    var xy = [];
    var zuobiaoPath="/sdcard/脚本/zuobiao21.txt";
    if (files.exists(zuobiaoPath)) {
       eval(files.read(zuobiaoPath));//快速适配分辨率
    } else {
        setScreenMetrics(1080, 2400); //默认分辨率，以下按键位置基于此分辨率
        var x = [572, 780, 990, 1196, 1410, 1620, 1828];
        var y = [960, 792, 625];
        for(var i = 0; i < 21; i++) {xy.push(x[i % 7], y[parseInt(i / 7)])}
    };
    function ran(){return Math.random()*20-10};
    function pre(id,c){while (s != 1) {sleep(100)};if(c==undefined){c=1};press(xy[id*2-2]+ran(),xy[id*2-1]+ran(),c)}
    function Z(t) {pre(1,t)};
    function X(t) {pre(2,t)};
    function C(t) {pre(3,t)};
    function V(t) {pre(4,t)};
    function B(t) {pre(5,t)};
    function N(t) {pre(6,t)};
    function M(t) {pre(7,t)};
    function A(t) {pre(8,t)};
    function S(t) {pre(9,t)};
    function D(t) {pre(10,t)};
    function F(t) {pre(11,t)};
    function G(t) {pre(12,t)};
    function H(t) {pre(13,t)};
    function J(t) {pre(14,t)};
    function Q(t) {pre(15,t)};
    function W(t) {pre(16,t)};
    function E(t) {pre(17,t)};
    function R(t) {pre(18,t)};
    function T(t) {pre(19,t)};
    function Y(t) {pre(20,t)};
    function U(t) {pre(21,t)};
    sleep(100);var window = floaty.window('<frame><vertical><button id="btn" text="暂停"/><horizontal><button id="speedLow" text="减速" w="80"/><button id="speedHigh" text="加速"w="80"/></horizontal><horizontal><button id="speed" text="x1" w="80"/><button id="stop" text="停止"w="80"/></horizontal></vertical></frame>');window.exitOnClose();
    window.btn.click(()=>{if (window.btn.getText() != '暂停') {s = 1;window.btn.setText('暂停')} else {s = 0;window.btn.setText('继续')}})
    window.speedHigh.click(()=>{speedControl=(speedControl*10+1)/10;window.speed.setText("x"+speedControl)})
    window.speedLow.click(()=>{if(speedControl<=0.1){return};speedControl=(speedControl*10-1)/10;window.speed.setText("x"+speedControl)})
    window.speed.click(()=>{speedControl=1;window.speed.setText("x"+speedControl)})
    window.stop.click(()=>{engines.stopAll()});
    function t(time) {sleep(time/speedControl)};"""

    KEY_MAP = {48: "Z", 50: "X", 52: "C", 53: "V", 55: "B", 57: "N", 59: "M", 60: "A", 62: "S", 64: "D", 65: "F",
               67: "G", 69: "H", 71: "J", 72: "Q", 74: "W", 76: "E", 77: "R", 79: "T", 81: "Y", 83: "U"}

    @staticmethod
    def sort(str_sort):
        """音符排序"""
        order = ["Q", "W", "E", "R", "T", "Y", "U", "A", "S", "D", "F", "G", "H", "J", "Z", "X", "C", "V", "B", "N",
                 "M"]
        return ''.join(sorted(str_sort, key=lambda x: order.index(x)))

    @staticmethod
    def find_all_indexes(input_string, character):
        """
        查找索引匹配索引
        :param input_string: 字符串
        :param character: 要查找的字符
        :return: 索引列表
        """
        indexes = []
        start = -1
        while True:
            start = input_string.find(character, start + 1)
            if start == -1:
                return indexes
            indexes.append(start)

    @staticmethod
    def get_number(string, key):
        """
        获取midi中msg信息中的参数
        :param string: msg信息 str
        :param key: 字段 str
        :return: 获取到的数值，错误返回None int
        """
        index = string.find(key) + len(key)
        tmp = ""
        try:
            while True:
                if string[index].isdigit():
                    tmp += string[index]
                    index += 1
                else:
                    break
        except Exception as e:
            print(e)
        if tmp != "":
            return int(tmp)
        else:
            return None

    @staticmethod
    def customSort(string, rvs=False):
        """
        排序琴键
        :param string: 带排序琴键
        :param rvs: 默认False，设置为True可以倒序
        :return: 排序后字符
        """
        order = "QWERTYUASDFGHJZXCVBNM"
        for char in string:
            if char not in order:
                return string
        if rvs:
            order = order[::-1]
        return ''.join(sorted(string, key=lambda x: order.index(x)))

    @staticmethod
    def get_keys(file, rvs=False):
        """
        midi转键盘
        :param file: midi文件路径 str
        :param rvs:  同时按的按键顺序反转
        :return: 呱格式，刻师傅时间，最短时间
        """
        mid = MidiFile(file)
        min_list = mid.tracks
        validData = []
        timeTmp = "tempo=600000"
        for i in min_list[0]:
            if "tempo" in str(i):
                timeTmp = str(i)
        speed = Midi.get_number(timeTmp, "tempo=") / 1000000
        # 检测各轨道是否有琴键，如果有将轨道放入validData
        for i in min_list:
            for j in i:
                if str(j)[:6] == "note_o":
                    validData.append(i)
                    break
        # 获取中间格式个最短时间并放在列表对应索引位置
        midData = []
        minTime = []
        for i in validData:
            tmp = Midi.transverter(i)
            midData.append(tmp[0])
            minTime.append(tmp[1])
        timeMin = minTime[0]
        for i in minTime:
            timeMin = gcd(timeMin, int(i))
        # 将各音轨转成呱的格式
        dataGua = []
        for i in midData:
            dataGua.append(Midi.tmpToGua(i, timeMin))
        # 合并各轨道
        data = dataGua[0]
        if len(dataGua) > 1:
            for i in range(1, len(dataGua)):
                data = Midi.addData(data, dataGua[i])
        # 括号内排序
        dataTmp = ""
        data01 = ""
        for i in data:
            if i == "=":
                data01 += Midi.customSort(dataTmp, rvs)
                dataTmp = ""
            else:
                dataTmp += i
                continue
            data01 += i
        data01 += Midi.customSort(dataTmp, rvs)
        data = Midi.GuaFormat(data01)
        return data, speed, timeMin

    @staticmethod
    def transverter(mid_data):
        """
        将单个轨道翻译成中间格式并返回
        :param mid_data: 单轨道数据
        :return: 中间格式，最短时间
        """
        data = ""
        time_tmp = 0
        for i in mid_data:
            note = str(i) + " "
            try:
                if note[:7] == "note_on":
                    time_tmp += Midi.get_number(note, "time=")
                    note_tmp = Midi.get_number(note, "note=")
                    if note_tmp not in Midi.KEY_MAP.keys():
                        continue
                    if time_tmp != 0:
                        data += str(time_tmp) + Midi.KEY_MAP[note_tmp]
                    else:
                        data += Midi.KEY_MAP[note_tmp]
                    time_tmp = 0
                elif note[:7] == "note_of":
                    time_tmp += Midi.get_number(note, "time=")
            except Exception as e:
                print(e)
                msg = "超出了原琴音域或存在黑键！"
                return msg
        # 去掉最前面的数字
        # while True:
        #     if data[0].isdigit():
        #         data = data[1:]
        #     else:
        #         break
        time_list = []
        t_tmp = ""
        for i in data:
            if i.isdigit():
                t_tmp += i
            elif t_tmp.isdigit():
                time_list.append(int(t_tmp))
                t_tmp = ""
        time_min = time_list[0]
        for i in time_list:
            time_min = gcd(time_min, i)
        return data, time_min

    @staticmethod
    def addData(data01, data02):
        """
        合并轨道呱格式琴谱
        :param data01:
        :param data02:
        :return: 合并后的琴谱
        """
        index01 = Midi.find_all_indexes(data01, "=")
        index02 = Midi.find_all_indexes(data02, "=")
        # 将短的放在dataTmp01
        if len(index02) < len(index01):
            dataTmp01 = data02
            dataTmp02 = data01
            tmp = index01.copy()
            index01 = index02.copy()
            index02 = tmp.copy()
        else:
            dataTmp01 = data01
            dataTmp02 = data02
        # 开始合并
        dataAdd = ""
        tmp01 = 0
        tmp02 = 0
        for i in range(len(index01)):
            dataTmp = dataTmp01[tmp01:index01[i]] + dataTmp02[tmp02:index02[i]]
            dataAdd += Midi.sort(dataTmp) + "="
            tmp01 = index01[i] + 1
            tmp02 = index02[i] + 1
        dataAdd += dataTmp01[tmp01:] + dataTmp02[tmp02:]
        return dataAdd

    @staticmethod
    def tmpToGua(data, time_min):
        """
        中间格式转呱不换行只有=
        :param data: 中间格式的数据
        :param time_min: 最短时间
        :return: 呱格式不换行只有=
        """
        t_tmp = ""
        data_key = ""
        for i in data:
            if i.isdigit():
                t_tmp += i
            elif t_tmp.isdigit():
                data_key += "=" * int(int(t_tmp) / time_min)
                data_key += i
                t_tmp = ""
            else:
                data_key += i
        return data_key

    @staticmethod
    def GuaFormat(data_key):
        """
        对呱格式没有换行，只有=的进行格式处理
        :param data_key: 格式化前
        :return: 格式化后
        """
        # 换行
        data = ""
        tmp_num = 0
        for i in data_key:
            data += i
            if i == "=":
                tmp_num += 1
            if tmp_num == 16:
                data += "\n"
                tmp_num = 0
        data += "=" * (16 - tmp_num)
        data_arr = data.split("\n")
        data = ""
        for i in range(len(data_arr)):
            data_arr[i] = data_arr[i].replace("====", "+").replace("==", "-")
            data += data_arr[i] + "\n"
        return data

    @staticmethod
    def get_midKey(file):
        """
        通过mid文件获取键盘按键，延迟用=表示
        :param file: mid文件路径
        :return: 键盘按键，时间间隔
        """
        data = Midi.get_keys(file)
        return data[0].replace("\n", "").replace("+", "====").replace("-", "=="), data[2] / 700
