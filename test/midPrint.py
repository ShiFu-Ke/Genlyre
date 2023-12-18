# @ Created with PyCharm Professional 2021.2.1
# @ Author KeShiFu
# @ Date 2023/09/15
# @ Time 9:37
import mido

mid = mido.MidiFile("E:\\桌面\\爸爸的雷达.mid")
mid1 = mido.MidiFile("E:\\桌面\\爸爸的雷达01.mid")
print(len(mid.tracks))
print(mid1.tracks)
