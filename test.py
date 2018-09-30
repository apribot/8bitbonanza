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

    #need to generate a longer sample and feed frames from it sequentially
    #otherwise we are stuck with tones over evolving sounds

    #for t in range(0,4410,1): sample.append(  ((t/2) * (t/3)) % 255  )
    #for t in range(0,4410,1): sample.append(  (t % 255  ))
    #for t in range(0,4410,1): sample.append( ((t%118|t%177) % 255  ))
    for t in range(0,4410,1): sample.append( (t*(t<<3|t>>1)) % 255  )
    #for t in range(0,4410,1): sample.append( (t%118|t%177) % 255  )
    #for t in range(0,4410,1): sample.append( ((((t%16)<<6)/8|t%255|t)-12) % 255  )
    raw = ''.join(map(chr, pitchShift(sample, noteoffset)))

    # dirty padding
    if(len(raw) < 4410):
        raw = raw * int(4410.0 / len(raw))

    data = raw
    return (data, pyaudio.paContinue)

def playNote(offset, sleep = 0.5):
    global noteoffset
    noteoffset = offset
    stream.start_stream()
    time.sleep(sleep)
    stream.stop_stream()

stream=pyaudio.PyAudio().open(
    format=pyaudio.paInt8,
    channels=1,
    rate=44100,
    output=True,
    stream_callback=callback)

playNote(0+12, 0.12)
playNote(4+12, 0.12)
playNote(7+12, 0.12)
playNote(11+12, 0.12)
playNote(12+12, 0.12)
playNote(11+12, 0.12)
playNote(7+12, 0.12)
playNote(4+12, 0.12)
playNote(0+12, 0.12)
playNote(4+12, 0.12)
playNote(7+12, 0.12)
playNote(11+12, 0.12)
playNote(12+12, 0.12)
playNote(11+12, 0.12)
playNote(7+12, 0.12)
playNote(4+12, 0.12)
playNote(-1+12, 0.12)
playNote(4+12, 0.12)
playNote(7+12, 0.12)
playNote(11+12, 0.12)
playNote(12+12, 0.12)
playNote(11+12, 0.12)
playNote(7+12, 0.12)
playNote(4+12, 0.12)
playNote(-1+12, 0.12)
playNote(4+12, 0.12)
playNote(7+12, 0.12)
playNote(11+12, 0.12)
playNote(12+12, 0.12)
playNote(11+12, 0.12)
playNote(7+12, 0.12)
playNote(4+12, 0.12)

stream.close()
pyaudio.PyAudio().terminate()