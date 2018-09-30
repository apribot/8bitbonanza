#square wave 1khz function generation

# The only import required...
import pyaudio

import numpy as np

def LInterp( x, a, n ):
    if( x <= 0 ):  return a[0];
    if( x >= n - 1 ):  return a[n-1];
    j = int(x)
    return a[j] + (x - j) * (a[j+1] - a[j])

def LInterpArray( a, n, m ):
    step = float( n - 1 ) / (m - 1)
    b = []
    for j in xrange(0,m):
        b.append(int(LInterp( j*step, a, n )))
    return b

def pitchShift(a, offset):
	n = len(a)

	factor = 2**(1.0 * offset / 12.0)
	m = int( (1.0 / factor) * n  )

	return LInterpArray(a, n, m)



# Initialise the only _variable_ in use...
n=0

# Set up a basic user screen...
# This assumes the minimum default 80x24 Terminal window size...

# Open the stream required, mono mode only...
stream=pyaudio.PyAudio().open(format=pyaudio.paInt8,channels=1,rate=16000,output=True)

# Now generate the 1KHz signal at the speakers/headphone output for about 15 seconds...
# Sine wave, to 8 bit depth only...




#for t in range(0,200,1): print (((t)*(t)) % 255)

sample = []

for t in range(0,1000,1): sample.append(  ((t/2) * (t/3)) % 255  )

for n in range(0,20,1): stream.write(''.join(map(chr, pitchShift(sample, 0))))

for n in range(0,20,1): stream.write(''.join(map(chr, pitchShift(sample, 4.0))))
for n in range(0,20,1): stream.write(''.join(map(chr, pitchShift(sample, 7.0))))

#map(chr, pitchShift(sample, 0))

#sample = map(chr, pitchShift(sample, 1, 1, 1))
#print('final')
#print (sample)

#for n in range(0,100,1): stream.write(''.join(sample))


'''
print('triangle')
for n in range(0,400,1): stream.write(triangle)

print('saw')
for n in range(0,400,1): stream.write(saw)

print('square')
for n in range(0,400,1): stream.write(square)
'''
# Close the open _channel(s)_...
stream.close()
pyaudio.PyAudio().terminate()

# End of 1KHz_SW_OSX.py program...
# Enjoy finding simple solutions to often very difficult problems... ;o)