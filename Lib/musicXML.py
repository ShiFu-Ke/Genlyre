# @ Created with PyCharm Community Edition
# @ Author KeShiFu
# @ Date 2023/05/19
# @ Time 14:39
from music21 import converter

# 将MIDI文件读取为music21对象
midi_data = converter.parse('Summer.mid')

# 将music21对象保存为MusicXML文件
midi_data.write('musicxml', 'example.xml')



