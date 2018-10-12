require 'love'
require 'love.filesystem'
require 'love.thread'
require 'love.sound'

table.insert = function(t, ...) 
	local arg = {...}
	for i = 1, #arg do
	
		t[#t+1] = arg[i] 
		
	end
	
end

local self = love.thread.getThread()

local soundData = self:get 'soundData'
local filename  = self:get 'filename'


local data = {}

data.bits = 16
data.channels = soundData:getChannels()
data.sampleRate = soundData:getSampleRate()
data.size = soundData:getSize()
data.length = data.size/(data.bits/8)
local length = data.length

local subchunk2size = length*data.bits/8
local chunksize = subchunk2size+36

--self:set('doing', 'analyzing')

--[[
for i = 1, math.ceil(length/2)*2 do

--	local n = soundData:getSample(i-1)
--	data[i] = n
--	self:set('n', i)
	data[i] = soundData:getSample(i-1)
	
end--]]

self:set('doing', 'headers')

local hex = '%04x'
local hex2= '%08x'

str = setmetatable({}, {__index = table})

str:insert('RIFF')
local chunkSize = hex2:format(chunksize)
local chunks = {tonumber(chunkSize:sub(1, 2), 16), tonumber(chunkSize:sub(3, 4), 16), tonumber(chunkSize:sub(5, 6), 16), tonumber(chunkSize:sub(7, 8), 16)}
str:insert(string.char(chunks[4]), string.char(chunks[3]), string.char(chunks[2]), string.char(chunks[1]))
str:insert "WAVE"
str:insert "fmt "
str:insert(string.char(16), string.char(0), string.char(0), string.char(0))
str:insert(string.char(1), string.char(0))--pcm
local channels = hex:format(data.channels)
channels = {tonumber(channels:sub(1, 2), 16), tonumber(channels:sub(3, 4), 16)}
str:insert(string.char(channels[2]), string.char(channels[1]))--variable channels!
--str:insert(string.char(2), string.char(0))--channels
local sampleRate = hex2:format(data.sampleRate)
sampleRate = {tonumber(sampleRate:sub(1, 2), 16), tonumber(sampleRate:sub(3, 4), 16), tonumber(sampleRate:sub(5, 6), 16), tonumber(sampleRate:sub(7, 8), 16)}
str:insert(string.char(sampleRate[4], sampleRate[3], sampleRate[2], sampleRate[1]))--variable sample rate!
--str:insert(string.char(68), string.char(172), string.char(0), string.char(0))--44100
local bitRate = hex2:format(data.sampleRate*data.channels*data.bits/8)
bitRate = {tonumber(bitRate:sub(1, 2), 16), tonumber(bitRate:sub(3, 4), 16), tonumber(bitRate:sub(5, 6), 16), tonumber(bitRate:sub(7, 8), 16)}
str:insert(string.char(bitRate[4], bitRate[3], bitRate[2], bitRate[1]))--variable bitrate!
--str:insert(string.char(0x10), string.char(0xb1), string.char(0x02), string.char(0x00)) --44100*2*16/8
local blockAlign = hex:format(data.channels*data.bits/8)
blockAlign = {tonumber(blockAlign:sub(1, 2), 16), tonumber(blockAlign:sub(3, 4), 16)}
str:insert(string.char(blockAlign[2], blockAlign[1]))
--str:insert(string.char(4), string.char(0))
local bits = hex:format(data.bits)
bits = {tonumber(bits:sub(1, 2), 16), tonumber(bits:sub(3, 4), 16)}
str:insert(string.char(bits[2], bits[1]))
--str:insert(string.char(16), string.char(0))
str:insert 'data'
local Subchunk2Size = subchunk2size
Subchunk2Size = hex2:format(Subchunk2Size)
Subchunk2Size = {tonumber(Subchunk2Size:sub(1,2), 16), tonumber(Subchunk2Size:sub(3,4), 16), tonumber(Subchunk2Size:sub(5,6), 16), tonumber(Subchunk2Size:sub(7,8), 16)}
Subchunk2Size = string.char(Subchunk2Size[4], Subchunk2Size[3], Subchunk2Size[2], Subchunk2Size[1])
str:insert(Subchunk2Size)

self:set('doing', 'samples')

for i = 1, math.ceil(length/2)*2 do

	sample = soundData:getSample(i-1)*(2^(data.bits-1.5))
	sampleHex = hex2:format(sample)
	sampleHex = {tonumber(sampleHex:sub(5,6), 16),tonumber(sampleHex:sub(7,8), 16)}
	str:insert(string.char(sampleHex[2]), string.char(sampleHex[1]))

end

self:set('doing', 'saving')

local f = love.filesystem.newFile(filename)
f:open 'w'
f:write(str:concat())
f:close()

self:set('length', #str)

self:set('done', true)

self:set('doing', 'nothing')

return