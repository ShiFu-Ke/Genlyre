# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/03/17
# @ Time 23:54
from Lib.MusicScore import MusicScore

text_yi = "as (fe) f rv cdv (cd) dfgv l"
print(MusicScore.yiToGua(text_yi, 100)[0])
text_gua = """
A=S-FE==F-R=V-C=D=V-CD-
D=F=G=V==L-=++
"""
print(MusicScore.GuaToYi(text_gua, 100)[0])
print(MusicScore.GuaToke(text_gua, 100)[0])
