local Wave = {}

Wave.save = function(self, soundData, filename)

	if self.Thread then
	
		error 'A saving is already in progress! It should be fine, if you don\'t close this.'
		
	end

	self.Thread = love.thread.newThread('waveSave', 'theWave/thread.lua')
	
	self.Thread:set('soundData', soundData)
	self.Thread:set('filename', filename)
	self.Thread:start()
	self.soundData = soundData
	self.filename = filename
	
end


Wave.update = function(self)

	if self.Thread then
	
		local done = self.Thread:get 'done'
		
		if self.Thread:peek 'error' then error(self.Thread:peek 'error') end
		
		if done then
		
			self.Thread:wait()
			self.Thread = nil
			
			if self.done then self.done(love.filesystem.getSaveDirectory()..'/'..self.filename) end
			
		end
		
		
	end
	
end




return Wave