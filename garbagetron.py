#sudo apt-get install ffmpeg libavcodec-extra
#sudo pip3 install pydub


from pydub import AudioSegment
samplePath = 'test/'
samples = 1000 * 255

def offsetToNote(offset):
	offset = offset + (5 * 12)
	notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
	return notes[offset%12] + str(int(offset/12))

def getWavePoint(t):
	a = t
	b =  t*(t << 4 & t >> 2)
	return int((a+b)/2)

def getWave(length):
	outp = ''
	for t in range(1,length):
		outp+=chr(getWavePoint(t%255))
	return outp

def writeWaveAtPitch(snd, instrumentName, noteOffset):
	factor = 2.0 ** (1.0 * noteOffset / 12.0)
	new_sample_rate = int(snd.frame_rate * factor)
	shifted_sound = snd._spawn(snd.raw_data, overrides={'frame_rate': new_sample_rate})
	shifted_sound = shifted_sound.set_frame_rate(44100)
	shifted_sound.export(samplePath + instrumentName + "_" + offsetToNote(noteOffset) + ".wav", format="wav")

sound = AudioSegment(
    data=getWave(samples).encode(),
    sample_width=1,
    frame_rate=44100,
    channels=1
)

#       1   3       6   8  10
#   |  |_| |_|  |  |_| |_| |_|  |  |_
#   |___|___|___|___|___|___|___|___|
#     0   2   4   5   7   9  11 

print('generating')
for noteoffset in range( (-4*12), (4*12)+1, 1):
	writeWaveAtPitch(sound, 'test', noteoffset)
	print(offsetToNote(noteoffset) + ' ', end="", flush=True)
print('done')