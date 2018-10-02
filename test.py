import pyaudio
import numpy as np
import time
import math

noteoffset = 0
frameptr = 0
waveforms = {}
rawsize = 44100

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

def setWaveform():
    global waveforms
    global rawsize
    waveforms = {}
    #for t in range(0,4410,1): sample.append(  ((t/2) * (t/3)) % 255  )
    #for t in range(0,4410,1): sample.append(  (t % 255  ))
    #for t in range(0,4410,1): sample.append( ((t%118|t%177) % 255  ))
    #for t in range(0,4410,1): sample.append( (t*(t<<3|t>>1)) % 255  )
    #for t in range(0,4410,1): sample.append( (t%118|t%177) % 255  )
    #for t in range(0,4410,1): sample.append( ((((t%16)<<6)/8|t%255|t)-12) % 255  )

    #for t in range(0,rawsize,1): waveform.append(  ((t/2) * (t/3)) % 255  )

    #just going to pre-provision the sounds because the pyaudio dox suck ass
    #and i have no idea what i'm doing
    for noteoffset in range(-4*12,(4*12)+1, 1):
        waveform = []

        for t in range(0,rawsize,1): 
            waveform.append(  int( (math.sin(t)+1) * 254)  % 255  )

        raw = pitchShift(waveform, noteoffset)
        factor = 255.0 / max(raw)
        raw = [ int(x*factor) for x in raw] 

        waveforms[noteoffset] = ''.join(map(chr, raw))

        while (len(waveforms[noteoffset]) < rawsize):
            waveforms[noteoffset] = waveforms[noteoffset] * 2 

		# normalize
       



def audioFactory(frame_size): 
    global noteoffset
    global waveforms
    global frameptr
    global rawsize

    ret = waveforms[noteoffset][frameptr * frame_size : (frameptr * frame_size)+frame_size]

    frameptr = frameptr + 1
    frameptr = frameptr % int(rawsize/frame_size)

    return ret



def callback(in_data, frame_count, time_info, status):
    data = audioFactory(frame_count)

    return (data, pyaudio.paContinue)


def playNote(offset, sleep = 0.5):
    global noteoffset
    noteoffset = offset
    stream.start_stream()
    time.sleep(sleep)
    stream.stop_stream()




setWaveform()

stream=pyaudio.PyAudio().open(
    format=pyaudio.paInt8,
    channels=1,
    rate=44100,
    output=True,
    stream_callback=callback
    )



print('0')
playNote(0, 0.5)
playNote(2, 0.5)
playNote(4, 0.5)




stream.close()
pyaudio.PyAudio().terminate()