# distort() is more of a wavewrap, need to add genuine distortion
# need to add bitcrushing
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

def squarewave(t, duty):
	if t % 2 < 2 * duty:
		return -1.0
	else:
		return 1.0

def trianglewave(t):
	return abs(((t+1.0) % 4.0) - 2.0) - 1.0

def sawwave(t):
	return (t%(2.0)) - 1.0

# yeah, pt = 1.0 to -1.0


def wavefold(pt, amp):
	pt = pt * (amp+1.0);
	return abs(((pt+1.0) % 4.0) - 2.0) - 1.0

def distort(pt, amp):
	pt = pt * (amp+1.0);
	return ((pt+1) % 2.0) - 1.0

themax = -99999999
themin = 99999999

def makeWav(fileName, noteOffset, sawLvl, triangleLvl, squareLvl, squareDuty, subSquareLvl, subSquareDuty, subtriangleLvl, wavefoldLvl, distortLvl):

	global themax, themin

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
			i = i * 0.01
			t = i * factor

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

			prepoint = wavefold(prepoint, wavefoldLvl)
			prepoint = distort(prepoint, distortLvl)

			point = int((prepoint) * (max_amplitude / 2.0))

			point = point * 0.99

			if point > themax:
				themax = point

			if point < themin:
				themin = point

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

sawLvl           = 0.0

triangleLvl      = 1.0

squareLvl        = 0.0
squareDuty       = 0.25

subSquareLvl     = 0.0
subSquareDuty    = 0.50

subtriangleLvl   = 0.0

wavefoldLvl      = 0.0
distortLvl       = 0.5

offset = -24

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
	distortLvl
)

print('min', themin, 'max', themax)