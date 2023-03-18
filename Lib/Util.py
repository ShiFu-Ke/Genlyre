# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/18
# @ Time 22:24
class Util:
    """
    工具类
    """

    @staticmethod
    def lcm(a, b):
        """
        求两个数的最小公倍数
        :param a: 数字1
        :param b: 数字2
        :return: 最小公倍数
        """
        for i in range(min(a, b), 0, -1):
            if a % i == 0 and b % i == 0:
                return a * b // i
