PRG_BANKS = 2
CHR_BANKS = 2
# header + prg + chr
NEW_SIZE = 16 + 16384*PRG_BANKS + 8192*CHR_BANKS

rom = list(open('build/nestris.nes', 'rb').read())

# set submapper. this is the only actual patch
rom[8] = 0x50

# not strictly necessary for now, but just in case
patch = bytearray(
    [
        # intialize prg banks
        0xA9, # lda #$00
        0x00,
        0x8D, # sta $8000
        0x00,
        0x80,
        0x4A, # lsr A
        0x8D, # sta $8000
        0x00,
        0x80,
        0x4A, # lsr A
        0x8D, # sta $8000
        0x00,
        0x80,
        0x4A, # lsr A
        0x8D, # sta $8000
        0x00,
        0x80,
        0x4A, # lsr A
        0x8D, # sta $8000
        0x00,
        0x80,
        0x4C,  # jmp (addr filled in later)
    ]
)

target = 0xFF50
romtarget = target - 0x7FF0

patch.extend(rom[0x800C:0x800E])

# verify target is all zeroes
if rom[romtarget : romtarget + len(patch)] != [0] * len(patch):
    raise RuntimeError(
        f"ROM space at ${target:04x} through ${target+len(patch):04x} is in use"
    )

# rom[romtarget : romtarget + len(patch)] = patch
# 
# rom[0x800C] = target & 0xFF
# rom[0x800D] = target >> 8

with open('build/nestris.nes', 'wb') as f:
    f.write(bytearray(rom[:NEW_SIZE]))
