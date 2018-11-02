from pydub import AudioSegment
import struct
import wavfile
import json
import os

with open('stolen_presets.json') as json_data_file:
    config = json.load(json_data_file)

samples = 1000 * 255


def linearInterpolate( x, a, n ):
    if( x <= 0 ):      
        return a[0];
    if( x >= n - 1 ):  
        return a[n-1];
    j = int(x)
    return a[j] + (x - j) * (a[j+1] - a[j])

def linearInterpolateArray( a, n, m ):
    step = float( n - 1 ) / (m - 1)
    b = []
    for j in range(0,m):
        b.append(int(linearInterpolate( j*step, a, n )))
    return b

def pitchShift(a, offset):
    n = len(a)
    factor = 2**(1.0 * offset / 12.0)
    m = int((1.0 / factor) * n)
    return linearInterpolateArray(a, n, m)


def offsetToNote(offset):
	offset = offset + (5 * 12)
	notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
	return notes[offset%12] + str(int(offset/12))

def getWavePoint(t, formulaA, formulaB):
	a =  eval(formulaA)
	b =  eval(formulaB)
	return int((a+b)//2) % 255

def getWave(length, formulaA, formulaB):
	outp = bytearray()
	for t in range(1,int(length)):
		outp.append(getWavePoint(t, formulaA, formulaB))

	return outp

def writeWaveAtPitch(snd, noteOffset, samplePath):
	fileName = samplePath + '/' + str(noteOffset+(12*6)) + ".wav"
	factor = 2.0 ** (1.0 * noteOffset / 12.0)
	new_sample_rate = (int(snd.frame_rate * factor) // 2) * 2

	shifted_sound = snd._spawn(snd.raw_data, overrides={'frame_rate': new_sample_rate})
	shifted_sound = shifted_sound.set_frame_rate(44100)
	shifted_sound = shifted_sound.set_channels(2)
	shifted_sound = shifted_sound.set_sample_width(2)
	shifted_sound.export(fileName, format="wav")

	# filthy hack for looping :(
	thing = wavfile.read(
		fileName 
	)
	
	wavfile.write(
		fileName,
		thing[0],
		thing[1],
		loops=[
			{
				'cuepointid': 0,
				'datatype': 0,
				'start': 0,
				'end': len(thing[1]),
				'fraction': 0,
				'playcount': 0
			}
		]
	)



cnt = 0

for x in config:

	directory = str(cnt) + ' ' + x['name']
	print('generating ' + x['name'])

	sound = AudioSegment(
		data=getWave(samples, x['a'], x['b']),
		sample_width=1,
		frame_rate=44100,
		channels=1
	)

	if not os.path.exists(directory):
		os.makedirs(directory)
	
	for noteoffset in range( (-5*12), (4*12)+1, 1):
		writeWaveAtPitch(sound, noteoffset, directory)
		print(str(noteoffset+(12*6)) + ' ', end="", flush=True)

	print('\ndone')

	cnt = cnt+1
