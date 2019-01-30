offset           = 0

attack           = 100.0   # attack in... time(?)
decay            = 300.0   # decay in... time?
sustain          = 0.0     # sustain volume (0.0 - 1.0)


wavefoldLvl      = 0.0
wavewrapLvl      = 0.0
distortLvl		 = 0.0   
bitResolution    = 16      # 1 - 16

lowpassLvl       = 50

volumeLvl        = 0.95
#=============================================================

import sys
from settings1 import *
import os
import math

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


def sinewave(pt):
	return(math.sin(2.0 * math.pi * pt));

def wavefold(pt, amp):
	pt = pt * (amp+1.0);
	return abs(((pt+1.0) % 4.0) - 2.0) - 1.0

def wavewrap(pt, amp):
	pt = pt * (amp+1.0);
	return ((pt+1) % 2.0) - 1.0

def distort(pt, amp):
	pt = pt * (amp+1.0);
	if pt < -.99999:
		return -.99999
	elif pt > .99999:
		return 0.99999
	else:
		return pt

def envelope(t):
	global attack,decay,sustain

	response = 0
	if t <= (attack+0.1):
		response = ((1.0/(attack+0.1)) * t ) ** (1.0/3.0)
	elif t > (attack+0.1) and t <= (attack+0.1) + decay:
		response = ( 1.0 - math.sin(((t-(attack+0.1)) * (1/decay) )/2.0 * math.pi))
		if response < sustain:
			response = sustain
	else:
		response = sustain
	return response


snip = [0] * lowpassLvl
i = 0

def lowpass(pt, windowSize):
	global snip, i

	snip[i] = pt
	i = (i+1) % windowSize

	return sum(snip) / windowSize


def makeWav(fileName, noteOffset, wavefoldLvl, wavewrapLvl, distortLvl, bitResolution, lowpassLvl, volumeLvl):
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
			t = (i * 0.01) * factor

			mod1 = sinewave(t * 0.5) * 0.2
			mod2 = sinewave(t * 1.3) * 0.3 

			mod3 = sinewave(t * 1.0) * 0.2
			mod4 = sinewave(t * 2.6) * 0.2

			prepoint = (sinewave(t + mod1 + mod2) + sinewave(t + mod3 + mod4)) / 2.0

			if bitResolution < 16:
				prepoint = float(int(prepoint * ((2 ** bitResolution)/2))) / ((2 ** bitResolution)/2)

			if wavefoldLvl > 0:
				prepoint = wavefold(prepoint, wavefoldLvl)
		
			if wavewrapLvl > 0:
				prepoint = wavewrap(prepoint, wavewrapLvl)
	
			if distortLvl > 0:
				prepoint = distort(prepoint, distortLvl)

			prepoint = prepoint * envelope(t)

			if lowpassLvl > 1:
				prepoint = lowpass(prepoint, lowpassLvl)

			point = int((prepoint) * (max_amplitude / 2.0))

			point = point * volumeLvl

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

directory = 'TEST'

print('generating ' + directory)

if not os.path.exists(directory):
	os.makedirs(directory)

makeWav(
	directory + '/' + str(offset+(48)) + '.wav', 
	offset, 
	wavefoldLvl,
	wavewrapLvl,
	distortLvl,
	bitResolution,
	lowpassLvl,
	volumeLvl
)
