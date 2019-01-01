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
	if t % 256 < 256.0 * duty:
		return -1.0
	else:
		return 1.0

def sinewave(t):
	return math.sin(t / 256.0 * math.pi * 2.0)

def sawwave(t):
	return (t%(256.0))/(127.0/2.0)-1.0

# yeah, pt = 1.0 to -1.0
def distort(pt, amp):
	pt = pt * (amp+1.0);
	if pt > 1.0:
		pt = pt - ((pt - 1.0) * 2.0)
	if pt < -1.0:
		pt = pt - ((pt + 1.0) * 2.0)

	return pt

def makeWav(fileName, noteOffset, sawLvl, sineLvl, squareLvl, squareDuty, subSquareLvl, subSquareDuty, subSineLvl, distortion):

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

			sqr = squarewave(t, squareDuty)
			sin = sinewave(t)
			saw = sawwave(t)
			subsqr = squarewave((t+256)/2, subSquareDuty)
			subsin = sinewave((t+128)/2)

			divisor = (squareLvl + sineLvl + sawLvl + subSineLvl + subSquareLvl)

			prepoint = (  ( (sqr * squareLvl) + (sin * sineLvl) + (saw * sawLvl) + (subsqr * subSquareLvl) + (subsin * subSineLvl) ) / divisor  )
			prepoint = distort(prepoint, distortion)
			prepoint = ((prepoint + 1.0) / 2.0) * 255
			point = (prepoint * (max_amplitude / 255)) - (max_amplitude / 2)
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

sawLvl        = 1.0

sineLvl       = 0.0

squareLvl     = 1.0
squareDuty    = 0.25

subSquareLvl  = 0.0
subSquareDuty = 0.50

subSineLvl    = 1.0

distortion    = 1.0

offset = 0

makeWav(
	directory + '/' + str(offset+(48)) + '.wav', 
	offset, 
	sawLvl, 
	sineLvl, 
	squareLvl, 
	squareDuty,
	subSquareLvl, 
	subSquareDuty, 
	subSineLvl,
	distortion
)