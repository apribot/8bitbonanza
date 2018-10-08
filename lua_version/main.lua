local samples = 1000 * 265 --19999
local rate = 44100
local bits = 8
local channels = 1

function waveFunction(t)
	return t
end

function generateSample()
	soundData = love.sound.newSoundData( samples, rate, bits, channels )

	for t=1,samples-1 do
		position = ((((  waveFunction(t)  )%255)/127.5)-1)
		-- intermix -1 oct tone because fatness and because i wanna
		position = (position * 0.8) + (((((  waveFunction(t)  )%510)/255)-1) * 0.2)
		soundData:setSample(t, position)
	end

	sample = love.audio.newSource(soundData)
	sample:setLooping(true)

	return sample
end

function playNote(sound, noteOffset)
  love.audio.stop(sound)
  pitchMod = 2^(noteOffset / 12.0)
  sound:setPitch(pitchMod)
  sound:play()
end

function stopAll(sound)	
	love.audio.stop(sound)
end

sample = generateSample()


print('playing 1')
playNote(sample, 24)
love.timer.sleep( 1 )
print('playing 2')
playNote(sample, 0)
love.timer.sleep( 1 )
stopAll(sample)

-- forces this thing to terminate like a normal lua script
love.event.quit(0)


--https://github.com/SiENcE/lovemidi
-- this looks like the best bet