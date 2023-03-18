# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/17
# @ Time 23:54
from Lib.MusicScore import MusicScore

# text_yi = "as (fe) f rv cdv (cd) dfgv l"
# print("yi->gua:\n" + MusicScore.yiToGua(text_yi, 100)[0])
# text_gua = """
# A=S-FE==F-R=V-C=D=V-CD-
# D=F=G=V==La-=+ad=bnh=
# """
# print("gua->ke:\n" + str(MusicScore.GuaToke(text_gua, 121)[0]))
text_ke = """AS (FE)/FR/V CD/V (CD) /
DFGV/ A  /    /(AD)(BNH)  /"""
time = 0.456
arr = MusicScore.keToGua(text_ke, time)
print("转换前：\n" + text_ke + "\n速度：" + str(time) + "\n\n转换后：\n" + arr[0] + "\n速度：" + str(arr[1]))
print(MusicScore.FormatKe("L A S"))
