# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/17
# @ Time 23:54
from Lib.MusicScore import MusicScore

# text_yi = """100
# as (fe) f rv cdv (cd) dfgv l
# """
# print("yi->gua:\n" + MusicScore.yiToGua(text_yi))
# text_gua = """100
# A=S-FE==F-R=V-C=D=V-CD-
# D=F=G=V==La-=+ad=b===
# """
# print("gua->ke:\n" + str(MusicScore.guaToke(text_gua)))
# print("gua->yi:\n" + str(MusicScore.guaToYi(text_gua)))
# text_ke = """0.6
# AS (FE)/FR/V CD/V (CD) /
# DFGV/ A  /    /(AD)(BNH)  /"""
# print("转换前：\n" + text_ke + "\n\n转换后：\n" + MusicScore.keToGua(text_ke))
# print(MusicScore.formatKe("L A S"))

print(MusicScore.isKe("D:\\桌面\\1.txt")[1])
