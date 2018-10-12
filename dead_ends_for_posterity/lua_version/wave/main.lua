wave = require 'theWave'
if love._openConsole then love._openConsole() end --not needed
require 'repler'.load'' --repler isn't needed, I just like it; thanks Bartbes!
love.load = function()

	Decoder = love.sound.newDecoder('file.ogg', 65536*128)
	
	SoundData = love.sound.newSoundData(Decoder)
	
	Source = love.audio.newSource(SoundData)
	Source:setLooping(true)
	Source:play()
	
	wave:save(SoundData, 'yay.wav')
	t1 = os.clock()
	
end


love.update = function(dt)

	wave:update()
	
end


wave.done = function(path)

	Source:pause()
	
	t2 = os.clock()
	print('It took', t2-t1, 'seconds.')
	
end


love.keypressed = function(k, u)

	if k == ' ' then
	
		if Source:isPaused() then Source:play()
		else Source:pause() end
		
	elseif k == 'r' then
	
		Source:rewind()
		
	end
	
end