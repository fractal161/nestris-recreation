-- copied from https://stackoverflow.com/a/9080080 because lazy
function toBits(num,bits)
    -- returns a table of bits, most significant first.
    bits = bits or math.max(1, select(2, math.frexp(num)))
    local t = {} -- will contain the bits        
    for b = bits, 1, -1 do
        t[b] = math.fmod(num, 2)
        num = math.floor((num - t[b]) / 2)
    end
    return table.concat(t)
end

function log_write(addr, val)
	local frame_num = emu.getState()["ppu.frameCount"]
    emu.log(frame_num..": "..toBits(val, 8).." written to "..string.format("%x", addr))
end

emu.addMemoryCallback(log_write, 1, 0x4000, 0x400F)
