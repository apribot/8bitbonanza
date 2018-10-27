from pydub import AudioSegment
import struct

samplePath = 'test/'
samples = 100 * 255

def offsetToNote(offset):
	offset = offset + (5 * 12)
	notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
	return notes[offset%12] + str(int(offset/12))

def getWavePoint(t, formulaA, formulaB):
	a =  eval(formulaA)
	b =  eval(formulaB)
	return int((a+b)/2)

def getWave(length, formulaA, formulaB):
	outp = ''
	for t in range(1,length):
		outp+=chr(getWavePoint(t%255, formulaA, formulaB))
	return outp

def writeWaveAtPitch(snd, instrumentName, noteOffset):
	factor = 2.0 ** (1.0 * noteOffset / 12.0)
	new_sample_rate = int(snd.frame_rate * factor)
	shifted_sound = snd._spawn(snd.raw_data, overrides={'frame_rate': new_sample_rate})
	shifted_sound = shifted_sound.set_frame_rate(44100)
	shifted_sound = shifted_sound.set_channels(2)
	shifted_sound = shifted_sound.set_sample_width(2)
	shifted_sound.export(samplePath + str(noteOffset+(12*6)) + ".wav", format="wav")

	# filthy hack for looping :(
	# no idea if this works!
	endofloop = int(samples * factor) #maybe???
	fid = open(samplePath + str(noteOffset+(12*6)) + ".wav", 'ab')
	fid.write(b'smpl')
	size = 36 + 24
	fid.write(struct.pack('<iiiiiIiiii', size, 0, 0, 0, 0, 0, 0, 0, 1, 0))
	fid.write(struct.pack('<iiiiii', 0, 0, 0, endofloop, 0, 0))
	fid.close()





formulaA = 't'
formulaB = 't*(t << 4 & t >> 2)'

sound = AudioSegment(
    data=getWave(samples, formulaA, formulaB).encode(),
    sample_width=1,
    frame_rate=44100,
    channels=1
)

print('generating')
for noteoffset in range( (-5*12), (4*12)+1, 1):
	writeWaveAtPitch(sound, 'test', noteoffset)
	print(str(noteoffset+(12*6)) + ' ', end="", flush=True)
print('done')


