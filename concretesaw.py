lowpassLvl = 0
gainLvl    = 1.0

import sys
from settings1 import *
import os


def write_word(f, value, size = -1):
	#a hack because i can't do size = sizeof(value) in args i guess?
	if size == -1:
		size = sys.getsizeof(value)

	lst = []
	x = 0
	while x < size:
		lst.append(value & 0xFF)
		value >>= 8
		x = x + 1

	f.write(bytearray(lst))

def squarewave(t, duty = 0.5):
	if t % 256 < 256 * duty:
		return 255
	else:
		return 0 

def sinewave(t):
	return int((sin(t / 256.0 * pi() * 2) + 1) * (256/2))

def sawwave(t):
	return (t % (256/2)) * 2



snip = [0] * lowpassLvl
i = 0

def lowpass(pt, windowSize):
	global snip, i

	snip[i] = pt
	i = (i+1) % windowSize

	return int(sum(snip) / windowSize)



def makeWav(fileName, noteOffset, formulaA, formulaB, lowpassLvl, gainLvl):

	noteOffset = noteOffset - 4.5# pitch fix

	max_amplitude = 65536
	hz		      = 44100	 # samples per second

	factor = 2 ** (1.0 * noteOffset / 12.0)
	N = int((256 * 500) * (1.0 / factor))  # total number of samples

	# data chunk length must either be an even number or we have to write a pad byte to the header and i ain't about that life 
	if N % 2 != 0: #is odd
		N = N+1

	with open(fileName, 'wb+') as f:
		f.write(b'RIFF----WAVEfmt ')
		write_word( f,	   16, 4 )  # no extension data
		write_word( f,	    1, 2 )  # PCM - integer samples
		write_word( f,	    2, 2 )  # two channels (stereo file)
		write_word( f,     hz, 4 )  # samples per second (Hz)
		write_word( f, 176400, 4 )  # (Sample hz * BitsPerSample * Channels) / 8
		write_word( f,	    4, 2 )  # data block size (size of two integer samples, one for each channel, in bytes)
		write_word( f,	   16, 2 )  # number of bits per sample (use a multiple of 8)

		data_chunk_pos = f.tell()

		f.write(b'data----')	   # (chunk size to be filled in later)

		for i in range(0,N):
			t = int(i * factor)

			a = formulaA(t)
			b = formulaB(t)

			a = a % 255
			b = b % 255

			point = (((a + b) / 2) * (max_amplitude / 255)) - (max_amplitude / 2)

			if lowpassLvl > 1:
				point = lowpass(point, lowpassLvl)

			point = int(point * gainLvl)

			write_word( f, int(point), 2 )
			write_word( f, int(point), 2 )

	
		f.write(b'smpl')

		sampleperiod = int(1000000000.0 / hz)
		
		write_word( f,           60, 4 )  # size, baby. hard 60 because the number of fields isn't changing
		write_word( f,            0, 4 )  # manufacturer
		write_word( f,            0, 4 )  # product
		write_word( f, sampleperiod, 4 )  # sample period
		write_word( f,            0, 4 )  # midi unity note
		write_word( f,            0, 4 )  # midi pitch fraction
		write_word( f,            0, 4 )  # smpte format
		write_word( f,            0, 4 )  # smpte offset
		write_word( f,            1, 4 )  # num sample loops
		write_word( f,            0, 4 )  # sampler data
		# list of sample loops
		write_word( f, 0, 4 )  # cutepointid
		write_word( f, 0, 4 )  # datatype
		write_word( f, 0, 4 )  # start
		write_word( f, N, 4 )  # end
		write_word( f, 0, 4 )  # fraction
		write_word( f, 0, 4 )  # playcount

		


		file_length = f.tell()
		# Fix the data chunk header to contain the data size
		f.seek( data_chunk_pos + 4 )
		write_word( f, (N * 4), 4 )

		# Fix the file header to contain the proper RIFF chunk size, which is (file size - 8, minus the damn sample block i guess?) bytes
		f.seek( 0 + 4 );
		write_word( f, file_length - 8, 4 ) #some how the normal 8 padding isn't enough for SamplerBox, 24 appears to work 
		f.seek(file_length)


# debug just saw
#settings = {'0 saw':{'a': (lambda t : t*((t>>12|t>>8)&63&t>>4)), 'b': (lambda t: t*((t>>12|t>>8)&63&t>>4) )}}
settings = {'57 nova': {'a': (lambda t : t*((t>>7|t>>10)|84&t|t<<26)), 'b': (lambda t: t*((t>>7|t>>10)|84&t|t<<27))}}
#settings = {'23 GRIT BASS':{'a': (lambda t : (t>>t*t)^t), 'b': (lambda t: t)}}
#32 GRIT BASS is messed up. re-check wav standard... i thing we're missing
# padding or something

patches = settings.keys()
bleh = sorted(patches)

for key in bleh:
	directory = key
	formulaA = settings[key]['a']
	formulaB = settings[key]['b']

	print('generating ' + directory)

	if not os.path.exists(directory):
		os.makedirs(directory)

	# this needs to be made less insane, as does the note fix above
	for offset in range( -24, 36 ,12 ):
		print( str(offset+(48)) + ' ')
		makeWav(directory + '/' + str(offset+(48)) + '.wav', offset, formulaA, formulaB, lowpassLvl, gainLvl)

