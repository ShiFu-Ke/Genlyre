import mido

# 打开原始的MIDI文件
original_file = mido.MidiFile("E:\\桌面\\爸爸的雷达.mid")

# 创建一个新的MIDI文件
merged_file = mido.MidiFile()

# 创建一个新的音轨，用于叠加音符
merged_track = mido.MidiTrack()

# 遍历原始MIDI文件的每个音轨
for track in original_file.tracks:
    # 遍历音轨中的每个音符消息
    for message in track:
        # 如果消息是"note_on"类型，表示音符开启
        if message.type == 'note_on':
            # 获取当前时间点的所有音符消息
            current_notes = [msg for msg in merged_track if msg.time == message.time]
            # 如果当前时间点已经有音符消息，将它们与新的音符消息合并
            if current_notes:
                current_notes.append(message)
                merged_track[merged_track.index(current_notes[0]):] = current_notes
            else:
                merged_track.append(message)
                # 如果消息是"note_off"类型，表示音符关闭，直接添加到新的音轨中
        else:
            merged_track.append(message)

        # 将合并后的音轨添加到新的MIDI文件中
merged_file.tracks.append(merged_track)

# 保存合并后的MIDI文件
merged_file.save("E:\\桌面\\爸爸的雷达01.mid")