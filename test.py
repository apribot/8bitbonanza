import pyaudio
import numpy as np
import time
import math
import pygame
import pickle
import sys

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

def generateWaveform():
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
            waveform.append(  int( ( ((t*8|t>>3)+139)<<4)  % 255 ) )
            #waveform.append( int( (t/2) * (t/3)) % 255 )
            #waveform.append( int(t) % 255 )

        raw1 = pitchShift(waveform, noteoffset)
        #raw2 = pitchShift(waveform, noteoffset-12)
        raw3 = pitchShift(waveform, noteoffset-24)

        #depth = layerWaves(raw2, raw3)
        raw = layerWaves(raw3, raw1)

        waveforms[noteoffset] = ''.join(map(chr, raw))

        while (len(waveforms[noteoffset]) < rawsize):
            waveforms[noteoffset] = waveforms[noteoffset] * 2 

        # normalize
        # edit: nah
        print(noteoffset)

def layerWaves(raw1, raw2):
    buff = []

    for r1, r2 in zip(raw1, raw2):
        buff.append(int( (r1 + r2) / 2.0))     
    
    return buff

       
def writeWaveform(file):
    global waveforms

    with open(file, 'wb') as f:
        pickle.dump(waveforms, f)

def readWaveform(file):
    global waveforms

    with open(file, 'rb') as f:
        waveforms = pickle.load(f)

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

if len(sys.argv) == 1:
    print(' -o [file]   create new instrument\n -i [file]   load existing instrument\n\n');
if len(sys.argv) == 3 and sys.argv[1] == '-o':
    print('Generating instrument...')
    generateWaveform()
    writeWaveform(sys.argv[2])
    print('Done.')
elif len(sys.argv) == 3 and sys.argv[1] == '-i':
    print('Loading...')
    readWaveform(sys.argv[2])
    print('Done.')
    stream=pyaudio.PyAudio().open(
        format=pyaudio.paInt8,
        channels=1,
        rate=44100,
        output=True,
        stream_callback=callback
        )
    playNote(0, 1)
    playNote(1, 1)
    playNote(3, 1)
    playNote(4, 1)
    playNote(5, 1)
    playNote(6, 1)
    playNote(7, 1)
    playNote(8, 1)

    stream.close()
    pyaudio.PyAudio().terminate()
else:
    print('Invalid command.\n\n')
    print(' -o [file]   create new instrument\n -i [file]   load existing instrument\n\n');

'''
generateWaveform()

stream=pyaudio.PyAudio().open(
    format=pyaudio.paInt8,
    channels=1,
    rate=44100,
    output=True,
    stream_callback=callback
    )



playNote(0-36, 2)
playNote(4-36, 2)

playNote(0-24, 2)
playNote(4-24, 2)

playNote(0-12, 2)
playNote(4-12, 2)

playNote(0, 2)
playNote(4, 2)

playNote(0+12, 2)
playNote(4+12, 2)

playNote(0+24, 2)
playNote(4+24, 2)

playNote(0+36, 2)
playNote(4+36, 2)

#playNote(7-36, 0.5)
#playNote(11-36, 0.5)
#playNote(12-36, 0.5)



stream.close()
pyaudio.PyAudio().terminate()

'''