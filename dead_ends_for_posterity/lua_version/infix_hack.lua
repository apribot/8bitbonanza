
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

debug.setmetatable(0, {  -- create metatable for numbers
  __call = function(a, op)
   if op == '<<' then return function(b) return lshift(a,b) end
   elseif op == '>>' then return function(b) return rshift(a,b) end
   elseif op == '|' then return function(b) return bor(a,b) end
   elseif op == '&' then return function(b) return band(a,b) end

   end
  end
})

print((20) '>>' (1))