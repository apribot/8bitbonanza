sawLvl           = 1.0

triangleLvl      = 0.0

squareLvl        = 0.0
squareDuty       = 0.125

subSquareLvl     = 0.5
subSquareDuty    = 0.125

subtriangleLvl   = 0.0

wavefoldLvl      = 1.0
wavewrapLvl      = 1.0
distortLvl		 = 1.0

attack           = 20.0
decay            = 150.0
sustain          = 0.3


bitResolution    = 16

offset = -12

# need to re-figure out the math for pitch shifting

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
	return(2.0 * pi() * pt);


def squarewave(pt, duty):
	if pt % 2 < (2 * duty):
		return -0.999
	else:
		return 0.999

def trianglewave(pt):
	return abs(((((pt+0.25)*2)+0.5) % 4.0) - 2.0) - 1.0

def sawwave(pt):
	return (2.0-((pt+1)%(2.0))) - 1.0

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


#big, sustain, 1

def envelope(t):
	global attack,decay,sustain

	response = 0
	if t <= attack:
		response = ((1.0/attack) * t ) ** (1.0/3.0)
		#response = t / attack
	elif t > attack:
		#response = (((((sustain - 1.0) / decay) * (t - attack) + 1.0) - sustain) / (1.0 - sustain)) * (1 - sustain) + 1 
		response =  1.0 - ((t-attack) / (attack+decay))
		if response < sustain:
			response = sustain

	return response


def makeWav(fileName, noteOffset, sawLvl, triangleLvl, squareLvl, squareDuty, subSquareLvl, subSquareDuty, subtriangleLvl, wavefoldLvl, wavewrapLvl, distortLvl, bitResolution):

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
			sqr = squarewave(t, squareDuty)
			tri = trianglewave(t)
			saw = sawwave(t)
			subsqr = squarewave(t/2.0, subSquareDuty)
			subtri = trianglewave(t/2.0)

			divisor = (squareLvl + triangleLvl + sawLvl + subtriangleLvl + subSquareLvl)

			prepoint = (  
				( 
					(sqr * squareLvl) 
					+ (tri * triangleLvl) 
					+ (saw * sawLvl) 
					+ (subsqr * subSquareLvl) 
					+ (subtri * subtriangleLvl) 
				) 
				/ divisor  
			)

			if bitResolution < 16:
				prepoint = float(int(prepoint * ((2 ** bitResolution)/2))) / ((2 ** bitResolution)/2)

			if wavefoldLvl > 0:
				prepoint = wavefold(prepoint, wavefoldLvl)
		
			if wavewrapLvl > 0:
				prepoint = wavewrap(prepoint, wavewrapLvl)
	
			if distortLvl > 0:
				prepoint = distort(prepoint, distortLvl)

			prepoint = prepoint * envelope(t)


			point = int((prepoint) * (max_amplitude / 2.0))

			point = point * 0.95

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

#=============================================================


makeWav(
	directory + '/' + str(offset+(48)) + '.wav', 
	offset, 
	sawLvl, 
	triangleLvl, 
	squareLvl, 
	squareDuty,
	subSquareLvl, 
	subSquareDuty, 
	subtriangleLvl,
	wavefoldLvl,
	wavewrapLvl,
	distortLvl,
	bitResolution
)
