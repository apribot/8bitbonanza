import sys
import os
import math

class Butterworth:
	def __init__(self):
		self.outputHistory = [0] * 3
		self.inputHistory = [0] * 2

	def filter(self, frequency, sampleRate, passType, resonance):
		self.resonance = resonance
		self.frequency = frequency
		self.sampleRate = sampleRate
		self.passType = passType


		if self.passType == 'lp':
			self.c = 1.0 / math.tan(math.pi * frequency / sampleRate)
			self.a1 = 1.0 / (1.0 + resonance * self.c + self.c * self.c)
			self.a2 = 2 * self.a1
			self.a3 = self.a1
			self.b1 = 2.0 * (1.0 - self.c * self.c) * self.a1
			self.b2 = (1.0 - resonance * self.c + self.c * self.c) * self.a1
		elif self.passType == 'hp':
			self.c = math.tan(math.pi * frequency / sampleRate)
			self.a1 = 1.0 / (1.0 + resonance * self.c + self.c * self.c)
			self.a2 = -2 * self.a1
			self.a3 = self.a1
			self.b1 = 2.0 * (self.c * self.c - 1.0) * self.a1
			self.b2 = (1.0 - resonance * self.c + self.c * self.c) * self.a1
		print(self.c, self.a1, self.a2, self.a3, self.b1, self.b2)

	def update(self, newInput):
		newOutput = self.a1 * newInput + self.a2 * self.inputHistory[0] + self.a3 * self.inputHistory[1] - self.b1 * self.outputHistory[0] - self.b2 * self.outputHistory[1]

		self.inputHistory[1] = self.inputHistory[0]
		self.inputHistory[0] = newInput

		self.outputHistory[2] = self.outputHistory[1]
		self.outputHistory[1] = self.outputHistory[0]
		self.outputHistory[0] = newOutput
		return newOutput


class Engine:
	def __init__(self):
		self.passType = 'none'

	def write_word(self, f, value, size = -1):
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


	def sinewave(self, pt):
		return(math.sin(2.0 * math.pi * pt));

	def wavefold(self, pt, amp):
		pt = pt * (amp+1.0);
		return abs(((pt+1.0) % 4.0) - 2.0) - 1.0

	def wavewrap(self, pt, amp):
		pt = pt * (amp+1.0);
		return ((pt+1) % 2.0) - 1.0

	def distort(self, pt, amp):
		pt = pt * (amp+1.0);
		if pt < -.99999:
			return -.99999
		elif pt > .99999:
			return 0.99999
		else:
			return pt


	def envelope(self, t):
		response = 0
		if t <= (self.attack+0.1):
			response = ((1.0/(self.attack+0.1)) * t ) ** (1.0/3.0)
		elif t > (self.attack+0.1) and t <= (self.attack+0.1) + self.decay:
			response = ( 1.0 - math.sin(((t-(self.attack+0.1)) * (1/self.decay) )/2.0 * math.pi))
			if response < self.sustain:
				response = self.sustain
		else:
			response = self.sustain
		return response



	def lowpass(self, pt, windowSize):
		snip[i] = pt
		i = (i+1) % windowSize
		return sum(snip) / windowSize


	def makeWav(self, fileName, noteOffset):
		actualResonance = ((math.sqrt(2)) * (1.0 - self.resonance))
		noteOffset = noteOffset - 4.5# pitch fix
		max_amplitude = 65536
		hz			  = 44100	 # samples per second

		flt = Butterworth()
		
		if self.passType != 'none':
			flt.filter(self.frequency, 44100, self.passType, actualResonance)

		factor = 2 ** (1.0 * noteOffset / 12.0)
		N = int((256 * 500) * (1.0 / factor))  # total number of samples

		# data chunk length must either be an even number or we have to write a pad byte to the header and i ain't about that life 
		if N % 2 != 0: #is odd
			N = N+1

		with open(fileName, 'wb+') as f:
			f.write(b'RIFF----WAVEfmt ')
			self.write_word( f,	    16, 4 )  # no extension data
			self.write_word( f, 	 1, 2 )  # PCM - integer samples
			self.write_word( f,	  	 2, 2 )  # two channels (stereo file)
			self.write_word( f,	    hz, 4 )  # samples per second (Hz)
			self.write_word( f, 176400, 4 )  # (Sample hz * BitsPerSample * Channels) / 8
			self.write_word( f,		 4, 2 )  # data block size (size of two integer samples, one for each channel, in bytes)
			self.write_word( f,	    16, 2 )  # number of bits per sample (use a multiple of 8)

			data_chunk_pos = f.tell()

			f.write(b'data----')	   # (chunk size to be filled in later)

			for i in range(0,N):
				t = (i * 0.01) * factor

				mod1 = self.sinewave(t * 0.5) * 0.2
				mod2 = self.sinewave(t * 1.3) * 0.3 

				mod3 = self.sinewave(t * 1.0) * 0.2
				mod4 = self.sinewave(t * 2.6) * 0.2

				prepoint = (self.sinewave(t + mod1 + mod2) + self.sinewave(t + mod3 + mod4)) / 2.0

				if self.bitResolution < 16:
					prepoint = float(int(prepoint * ((2 ** self.bitResolution)/2))) / ((2 ** self.bitResolution)/2)

				if self.wavefoldLvl > 0:
					prepoint = self.wavefold(prepoint, self.wavefoldLvl)
			
				if self.wavewrapLvl > 0:
					prepoint = self.wavewrap(prepoint, self.wavewrapLvl)
		
				if self.distortLvl > 0:
					prepoint = self.distort(prepoint, self.distortLvl)

				if self.passType != 'none':
					prepoint = flt.update(prepoint)

				if prepoint > 0.99:
					prepoint = 0.99
				elif prepoint < -0.99:
					prepoint = -0.99

				prepoint = prepoint * self.envelope(t)

				point = int((prepoint) * (max_amplitude / 2.0))

				point = point * self.volumeLvl

				self.write_word( f, int(point), 2 )
				self.write_word( f, int(point), 2 )

			f.write(b'smpl')

			sampleperiod = int(1000000000.0 / hz)
			
			self.write_word( f,		      60, 4 )  # size, baby. hard 60 because the number of fields isn't changing
			self.write_word( f,			   0, 4 )  # manufacturer
			self.write_word( f,			   0, 4 )  # product
			self.write_word( f, sampleperiod, 4 )  # sample period
			self.write_word( f,			   0, 4 )  # midi unity note
			self.write_word( f,			   0, 4 )  # midi pitch fraction
			self.write_word( f,			   0, 4 )  # smpte format
			self.write_word( f,			   0, 4 )  # smpte offset
			self.write_word( f,			   1, 4 )  # num sample loops
			self.write_word( f,			   0, 4 )  # sampler data

			# list of sample loops
			self.write_word( f, 0, 4 )  # cutepointid
			self.write_word( f, 0, 4 )  # datatype
			self.write_word( f, 0, 4 )  # start
			self.write_word( f, N, 4 )  # end
			self.write_word( f, 0, 4 )  # fraction
			self.write_word( f, 0, 4 )  # playcount

			file_length = f.tell()

			# Fix the data chunk header to contain the data size
			f.seek( data_chunk_pos + 4 )
			self.write_word( f, (N * 4), 4 )

			# Fix the file header to contain the proper RIFF chunk size, which is (file size - 8, minus the damn sample block i guess?) bytes
			f.seek( 0 + 4 );
			self.write_word( f, file_length - 8, 4 )
			f.seek(file_length)


e = Engine()

#=====================================================

e.attack        = 0.0
e.decay         = 1300.0
e.sustain       = 0.0

e.wavefoldLvl   = 0.0
e.wavewrapLvl   = 0.0
e.distortLvl    = 0.0
e.bitResolution = 16

e.passType      = 'lp'
e.frequency     = 500
e.resonance     = .99 #0.0 to 1.0

e.volumeLvl     = 1.0

offset          = 0
directory       = 'TEST'

#=====================================================

print('generating ' + directory)

if not os.path.exists(directory):
	os.makedirs(directory)

fname = directory + '/' + str(offset+(48)) + '.wav'

e.makeWav(fname, offset)
