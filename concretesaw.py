import sys
from settings import *
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


def makeWav(fileName, noteOffset, formulaA, formulaB):

	noteOffset = noteOffset - 4.5# pitch fix

	max_amplitude = 65536
	hz		      = 44100	 # samples per second

	factor = 2 ** (1.0 * noteOffset / 12.0)
	N = int((256 * 500) * (1.0 / factor))  # total number of samples

	with open(fileName, 'wb+') as f:
		f.write("RIFF----WAVEfmt ")
		write_word( f,	 16, 4 )  # no extension data
		write_word( f,	  1, 2 )  # PCM - integer samples
		write_word( f,	  2, 2 )  # two channels (stereo file)
		write_word( f, hz, 4 )  # samples per second (Hz)
		write_word( f, 176400, 4 )  # (Sample hz * BitsPerSample * Channels) / 8
		write_word( f,	  4, 2 )  # data block size (size of two integer samples, one for each channel, in bytes)
		write_word( f,	 16, 2 )  # number of bits per sample (use a multiple of 8)

		f.write("smpl")

		sampleperiod = int(1000000000.0 / hz)
		
		write_word( f, 60, 4 ) # size, baby. hard 60 because the number of fields isn't changing
		write_word( f, 0, 4 )  # manufacturer
		write_word( f, 0, 4 )  # product
		write_word( f, sampleperiod, 4 ) # sample period
		write_word( f, 0, 4 )  # midi unity note
		write_word( f, 0, 4 )  # midi pitch fraction
		write_word( f, 0, 4 )  # smpte format
		write_word( f, 0, 4 )  # smpte offset
		write_word( f, 1, 4 )  # num sample loops
		write_word( f, 0, 4 )  # sampler data
		# list of sample loops
		write_word( f, 0, 4 )  # cutepointid
		write_word( f, 0, 4 )  # datatype
		write_word( f, 0, 4 )  # start
		write_word( f, N, 4 )  # end
		write_word( f, 0, 4 )  # fraction
		write_word( f, 0, 4 )  # playcount

	 	data_chunk_pos = f.tell()

		f.write("data----")	   # (chunk size to be filled in later)

		for i in range(1,N):
			t = int(i * factor)

			a = formulaA(t)
			b = formulaB(t)

			a = a % 255
			b = b % 255

			point = (((a + b) / 2) * (max_amplitude / 255)) - (max_amplitude / 2)

			write_word( f, point, 2 )
			write_word( f, point, 2 )

		file_length = f.tell()

		# Fix the data chunk header to contain the data size
		f.seek( data_chunk_pos + 4 )
		write_word( f, file_length - data_chunk_pos + 8 )

		# Fix the file header to contain the proper RIFF chunk size, which is (file size - 8) bytes
		f.seek( 0 + 4 );
		write_word( f, file_length - 8, 4 ) 


for key in settings:
	directory = key
	formulaA = settings[key]['a']
	formulaB = settings[key]['b']

	print('generating ' + directory)

	if not os.path.exists(directory):
		os.makedirs(directory)

	# this needs to be made less insane, as does the note fix above
	for offset in range( -12, 36 ,12 ):
		print( str(offset+(48)) + ' ')
		makeWav(directory + '/' + str(offset+(48)) + '.wav', offset, formulaA, formulaB)

