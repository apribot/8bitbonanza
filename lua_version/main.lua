
local samples = 19999
local rate = 44100
local bits = 8
local channels = 1

soundData = love.sound.newSoundData( samples, rate, bits, channels )


print('creating samples')

for t=1,samples-1 do
	soundData:setSample(t, ((((  (t/3) * (t/2)  )%255)/127.5)-1))
end
	
print('done')

sample = love.audio.newSource(soundData)

--src1:setVolume(0.9) -- 90% of ordinary volume
--src2:setVolume(0.7)

sample:play()
sample:rewind()
sample:setPitch(0.5) -- one octave lower
sample:play()
sample:rewind()
sample:setPitch(0.5) -- one octave lower
sample:play()
