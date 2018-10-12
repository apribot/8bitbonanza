local samples = 1000 * 265 --19999
local rate = 44100
local bits = 8
local channels = 1

-- love uses older version of luaJit, which doesn't support
-- bitwise infix ops, this is hella lame but love's support
-- of audio is so pleasant, so i make due.
local function lshift(a,b)
	return a * 2 ^ b
end

local function rshift(a,b)
	return math.floor(a / 2 ^ b)
end

local function bor(a,b)
	return a or b
end

local function band(a,b)
	return a and b 
end

debug.setmetatable(0, {
  __call = function(a, op)
   if op == '<<' then return function(b) return lshift(a,b) end
   elseif op == '>>' then return function(b) return rshift(a,b) end
   elseif op == '|' then return function(b) return bor(a,b) end
   elseif op == '&' then return function(b) return band(a,b) end
   end
  end
})

function waveFunction(t)
--	a = t*( (t) '<<' (4) '&' (t) '>>' (3))*( (t) '<<' (3) '|' (t) '>>' (1) '|' ( (t) '<<' (1)) '|' (t*t) '>>' (2))
--	b = t*( (t) '<<' (4) '&' (t) '>>' (2))

	a = t
	b =  t*( (t) '<<' (4) '&' (t) '>>' (2))
	return (a+b)/2
end

function generateSample()
	soundData = love.sound.newSoundData( samples, rate, bits, channels )

	for t=1,samples-1 do
		position = ((((  waveFunction(t)  )%255)/127.5)-1)
		-- intermix -1 oct tone because fatness and because i wanna
		--position = (position * 0.8) + (((((  waveFunction(t)  )%510)/255)-1) * 0.2)
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

--       1   3       6   8  10
--   |  |_| |_|  |  |_| |_| |_|  |  |_
--   |___|___|___|___|___|___|___|___|
--     0   2   4   5   7   9  11 
playNote(sample, 0)
love.timer.sleep( 0.2 )
playNote(sample, 4)
love.timer.sleep( 0.2 )
playNote(sample, 7)
love.timer.sleep( 0.2 )
playNote(sample, 11)
love.timer.sleep( 0.2 )
playNote(sample, 12)
love.timer.sleep( 0.2 )
playNote(sample, 11)
love.timer.sleep( 0.2 )
playNote(sample, 7)
love.timer.sleep( 0.2 )
playNote(sample, 4)
love.timer.sleep( 0.2 )
playNote(sample, 0)
love.timer.sleep( 0.2 )
playNote(sample, 4)
love.timer.sleep( 0.2 )
playNote(sample, 7)
love.timer.sleep( 0.2 )
playNote(sample, 11)
love.timer.sleep( 0.2 )
playNote(sample, 12)
love.timer.sleep( 0.2 )
playNote(sample, 11)
love.timer.sleep( 0.2 )
playNote(sample, 7)
love.timer.sleep( 0.2 )
playNote(sample, 4)
love.timer.sleep( 0.2 )
--[[
print('playing 24')
playNote(sample, 24)
love.timer.sleep( 1 )

print('playing 12')
playNote(sample, 12)
love.timer.sleep( 1 )

print('playing 0')
playNote(sample, 0)
love.timer.sleep( 1 )
stopAll(sample)

print('playing -12')
playNote(sample, -12)
love.timer.sleep( 1 )

print('playing -24')
playNote(sample, -24)
love.timer.sleep( 1 )
]]--
-- forces this thing to terminate like a normal lua script
stopAll(sample)

love.event.quit(0)


--https://github.com/SiENcE/lovemidi
-- this looks like the best bet