import hashlib
import os
import sys

'''
we use the addresses from the disassembly
'''

def get_prg_range(prg, start_addr, size=1):
    start = start_addr - 0x8000
    return prg[start:start+size]

def get_prg_byte(prg, addr):
    return get_prg_range(prg, addr, 1)

# the original rom uses a custom format that specifies a ppu row address, then
# a byte count, then a sequence of bytes. we just store everything directly
def extract_nametable(prg, start_addr):
    encoded_nt = get_prg_range(prg, start_addr, 32*35)
    nt = b''
    for i in range(32):
        nt += encoded_nt[3+35*i:35*i+35]
    return nt

# palettes are similar, but only involve one row so it's a little easier
def extract_palette(prg, start_addr):
    return get_prg_range(prg, start_addr+3, 0x20)

if __name__ == '__main__':
    dirs = [
        'skins/classic',
        'skins/classic/game',
        'skins/classic/legal',
        'skins/classic/level_menu',
        'skins/classic/title',
        'skins/classic/type_menu',
        'skins/classic/sfx',
    ]
    for d in dirs:
        if not os.path.exists(d):
            os.mkdir(d)
    if not os.path.exists('tetris.nes'):
        print('Please provide a copy of the original NTSC Tetris as tetris.nes')
        sys.exit(1)
    with open('tetris.nes', 'rb') as f:
        rom = f.read()
        EXPECTED_SHA1 = '77747840541bfc62a28a5957692a98c550bd6b2b'
        if hashlib.sha1(rom).hexdigest() != EXPECTED_SHA1:
            print(f'Provided tetris.nes does not have expected SHA1 of {EXPECTED_SHA1}')
            sys.exit(1)

        prg_size = rom[4] * 16384
        chr_size = rom[5] * 8192
        prg = rom[16:16+prg_size]
        chr = rom[16+prg_size:16+prg_size+chr_size]
    with open('skins/classic/default_high_scores.bin', 'wb+') as f:
        # the original rom stores all names, then all scores, then all levels,
        # while our format stores everything in sequence
        scores = get_prg_range(prg, 0xAD67, 0x50)
        for i in range(0, 6):
            idx = i
            # account for empty field
            if i > 2:
                idx += 1
            # name
            f.write(scores[6*idx:6*idx+6])
            # score (convert from big to little endian)
            f.write(scores[3*idx+50].to_bytes())
            f.write(scores[3*idx+49].to_bytes())
            f.write(scores[3*idx+48].to_bytes())
            # level
            f.write(scores[idx+72].to_bytes())
    with open('skins/classic/game/palette.pal', 'wb+') as f:
        f.write(extract_palette(prg, 0xACF3))
    with open('skins/classic/game/screen.nam', 'wb+') as f:
        nt = bytearray(extract_nametable(prg, 0xBF3C))
        # patch in A for a-type
        nt[32*4+3] = 0x0A
        f.write(nt)

    with open('skins/classic/leaderboard_charmap.bin', 'wb+') as f:
        f.write(get_prg_range(prg, 0xA08C, 44))

    with open('skins/classic/legal/palette.pal', 'wb+') as f:
        f.write(extract_palette(prg, 0xAD17))
    with open('skins/classic/legal/screen.nam', 'wb+') as f:
        f.write(extract_nametable(prg, 0xADB8))

    with open('skins/classic/level_menu/palette_a.pal', 'wb+') as f:
        # the original prg patches the highlight color
        palette = bytearray(extract_palette(prg, 0xAD2B))
        palette[10] = get_prg_byte(prg, 0xC95D+3)[0]
        f.write(palette)
    with open('skins/classic/level_menu/palette_b.pal', 'wb+') as f:
        f.write(extract_palette(prg, 0xAD2B))
    with open('skins/classic/level_menu/screen.nam', 'wb+') as f:
        f.write(extract_nametable(prg, 0xBADB))

    with open('skins/classic/tiles.chr', 'wb+') as f:
        f.write(chr)

    with open('skins/classic/title/palette.pal', 'wb+') as f:
        f.write(extract_palette(prg, 0xAD2B))
    with open('skins/classic/title/screen.nam', 'wb+') as f:
        f.write(extract_nametable(prg, 0xB219))

    with open('skins/classic/type_menu/palette.pal', 'wb+') as f:
        f.write(extract_palette(prg, 0xAD2B))
    with open('skins/classic/type_menu/screen.nam', 'wb+') as f:
        f.write(extract_nametable(prg, 0xB67A))

    # sfx!
    with open('skins/classic/sfx/menu_change.bin', 'wb+') as f:
        stride_bytes = get_prg_byte(prg, 0xE3CA+1)
        # init data
        f.write(stride_bytes)
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE124, 4))
        # stage 2
        f.write(stride_bytes)
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE128, 4))
        # finish
        f.write(b'\0')

    with open('skins/classic/sfx/menu_select.bin', 'wb+') as f:
        pass
        stride_bytes = get_prg_byte(prg, 0xE473+1)
        # init data
        f.write(stride_bytes)
        f.write(b'\x0F')
        init_data = get_prg_range(prg, 0xE12C, 4)
        f.write(init_data)
        vol = init_data[2]
        for i in range(3):
            f.write(stride_bytes)
            # 4002 and 4003
            f.write(b'\x0C')
            vol = vol - 1 - (vol // 16)
            f.write(vol.to_bytes())
            f.write(init_data[3].to_bytes())
        # finish
        f.write(b'\0')

    with open('skins/classic/sfx/shift_piece.bin', 'wb+') as f:
        stride_bytes = get_prg_byte(prg, 0xE390+6)
        # init data
        f.write(stride_bytes)
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE144, 4))
        # finish
        f.write(b'\0')

    with open('skins/classic/sfx/tetris_clear.bin', 'wb+') as f:
        stride_bytes1 = get_prg_byte(prg, 0xE403+1)
        # first phase init
        f.write(stride_bytes1)
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE130, 4))
        # TODO: unsure if necessary to rewrite other regs
        # first phase
        for i in range(8):
            f.write(stride_bytes1)
            f.write(b'\x05') # 4000 and 4002
            f.write(get_prg_byte(prg, 0xE4B0+i))
            f.write(get_prg_byte(prg, 0xE4C9+i))
        # second phase init
        stride_bytes2 = get_prg_byte(prg, 0xE42E+1)
        f.write(stride_bytes2)
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE138, 4))
        # second phase
        for i in range(8):
            f.write(stride_bytes2)
            f.write(b'\x05') # 4000 and 4002
            f.write(get_prg_byte(prg, 0xE4B0+i))
            f.write(get_prg_byte(prg, 0xE4B9+i))
        # finish
        f.write(b'\0')

    with open('skins/classic/sfx/rotate_piece.bin', 'wb+') as f:
        stride = int.from_bytes(get_prg_byte(prg, 0xE3D1+6))
        # init data
        f.write((2*stride-1).to_bytes())
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE114, 4))
        # stage 2
        f.write(stride.to_bytes())
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE114, 4))
        # stage 3
        f.write(stride.to_bytes())
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE118, 4))
        # finish
        f.write(b'\0')

    with open('skins/classic/sfx/level_up.bin', 'wb+') as f:
        stride_bytes = get_prg_byte(prg, 0xE4EC+1)
        # init data
        f.write(stride_bytes)
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE120, 4))
        # loop
        hi_byte = get_prg_byte(prg, 0xE4D1+19)
        for i in range(9):
            f.write(stride_bytes)
            f.write(b'\x0C') # 4002 and 4003
            f.write(get_prg_byte(prg, 0xE4F3+i))
            f.write(hi_byte)
        # finish
        f.write(b'\0')

    with open('skins/classic/sfx/lock_piece.bin', 'wb+') as f:
        stride_bytes = get_prg_byte(prg, 0xE384+6)
        # init
        f.write(stride_bytes)
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE120, 4))
        # finish
        f.write(b'\0')

    with open('skins/classic/sfx/tetris_end.bin', 'wb+') as f:
        # init
        stride_bytes = get_prg_byte(prg, 0xE42E+1)
        f.write(stride_bytes)
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE138, 4))
        for i in range(8):
            f.write(stride_bytes)
            f.write(b'\x05') # 4000 and 4002
            f.write(get_prg_byte(prg, 0xE4B0+i))
            f.write(get_prg_byte(prg, 0xE4B9+i))
        # finish
        f.write(b'\0')

    with open('skins/classic/sfx/line_clear.bin', 'wb+') as f:
        stride_bytes = get_prg_byte(prg, 0xE41A+1)
        # init
        f.write(stride_bytes)
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE134, 4))
        for i in range(8):
            f.write(stride_bytes)
            f.write(b'\x05') # 4000 and 4002
            f.write(get_prg_byte(prg, 0xE4B0+i))
            f.write(get_prg_byte(prg, 0xE4C1+i))
        # finish
        f.write(b'\0')

    with open('skins/classic/sfx/curtain.bin', 'wb+') as f:
        # init
        f.write(b'\1')
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE104, 4))
        for i in range(32):
            vol = int.from_bytes(get_prg_byte(prg, 0xE174+i))
            lo = int.from_bytes(get_prg_byte(prg, 0xE154+i))
            f.write(b'\1')
            f.write(b'\x05') # 400c and 400e
            f.write((0x10 + (vol // 16)).to_bytes())
            f.write((lo // 16).to_bytes())
            # skip last nybble
            if i < 31:
                f.write(b'\1')
                f.write(b'\x05') # 400c and 400e
                f.write((0x10 + (vol % 16)).to_bytes())
                f.write((lo % 16).to_bytes())
        # finish
        f.write(b'\0')

    with open('skins/classic/sfx/rocket.bin', 'wb+') as f:
        # init
        stride_bytes = get_prg_byte(prg, 0xE2CC+1)
        f.write(stride_bytes)
        f.write(b'\x0F')
        f.write(get_prg_range(prg, 0xE108, 4))
        # finish
        f.write(b'\0')

    with open('skins/classic/sfx/pause.bin', 'wb+') as f:
        # yea no clue where this is stored lmao
        stride_bytes = b'\4'
        f.write(stride_bytes)
        f.write(b'\x0F')
        # mute
        f.write(get_prg_byte(prg, 0xE271+6))
        f.write(get_prg_byte(prg, 0xE271+6))
        f.write(get_prg_byte(prg, 0xE271+6))
        f.write(get_prg_byte(prg, 0xE271+1))
        for i in range(2):
            f.write(stride_bytes)
            f.write(b'\x0F')
            f.write(get_prg_range(prg, 0xE110, 4))
            f.write(stride_bytes)
            f.write(b'\x0F')
            f.write(get_prg_range(prg, 0xE10C, 4))
        # finish
        f.write(b'\0')


