import pyaudio
import numpy as np
import time

noteoffset = 0

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
    for j in xrange(0,m):
        b.append(int(linearInterpolate( j*step, a, n )))
    return b

def pitchShift(a, offset):
    n = len(a)
    factor = 2**(1.0 * offset / 12.0)
    m = int((1.0 / factor) * n)
    return linearInterpolateArray(a, n, m)

def callback(in_data, frame_count, time_info, status):
    sample = []
    print(noteoffset)
    for t in range(0,2000,1): sample.append(  ((t/2) * (t/3)) % 255  )
    #for t in range(0,2000,1): sample.append(  (t % 255  ))

    raw = ''.join(map(chr, pitchShift(sample, noteoffset)))

    # dirty padding
    if(len(raw) < 2000):
    	raw = raw * int(2000.0 / len(raw))

    data = raw
    return (data, pyaudio.paContinue)

def playNote(offset):
	global noteoffset
	noteoffset = offset
	stream.start_stream()
	time.sleep(0.5)
	stream.stop_stream()

n=0

stream=pyaudio.PyAudio().open(
    format=pyaudio.paInt8,
    channels=1,
    rate=44100,
    output=True,
    stream_callback=callback)

playNote(0)
playNote(4)
playNote(7)



stream.close()
pyaudio.PyAudio().terminate()