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

first_frame = nil

function log(str)
    emu.log(str)
    print(str)
end

function log_write(addr, val)
    local frame_num = emu.getState()["ppu.frameCount"]
    if first_frame == nil then
        first_frame = frame_num
    end

    log((frame_num-first_frame)..": "..toBits(val, 8).." written to "..string.format("%x", addr))
end

function reset_first_frame()
    local frame_num = emu.getState()["ppu.frameCount"]
    if first_frame ~= nil and frame_num - first_frame > 120 then
        first_frame = nil
        log("---")
    end
end

emu.addMemoryCallback(log_write, 1, 0x4000, 0x400F)
emu.addEventCallback(reset_first_frame, emu.eventType.nmi)
