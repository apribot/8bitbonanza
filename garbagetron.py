from pydub import AudioSegment
samplePath = 'test/'
samples = 100 * 255

def offsetToNote(offset):
	offset = offset + (5 * 12)
	notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
	return notes[offset%12] + str(int(offset/12))

def getWavePoint(t):
	#a = t
	a =  t
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
	shifted_sound = shifted_sound.set_channels(2)
	shifted_sound = shifted_sound.set_sample_width(2)
	shifted_sound.export(samplePath + instrumentName + "_" + str(noteOffset+(12*6)) + ".wav", format="wav")

sound = AudioSegment(
    data=getWave(samples).encode(),
    sample_width=1,
    frame_rate=44100,
    channels=1
)

print('generating')
for noteoffset in range( (-5*12), (4*12)+1, 1):
	writeWaveAtPitch(sound, 'test', noteoffset)
	print(str(noteoffset+(12*6)) + ' ', end="", flush=True)
print('done')