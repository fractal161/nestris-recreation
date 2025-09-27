import hashlib
import os
import sys

'''
we use the addresses from the disassembly
'''

def get_prg_range(prg, start_addr, size=1):
    start = start_addr - 0x8000
    return prg[start:start+size]

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
        f.write(extract_nametable(prg, 0xBF3C))

    with open('skins/classic/leaderboard_charmap.bin', 'wb+') as f:
        f.write(get_prg_range(prg, 0xA08C, 44))

    with open('skins/classic/legal/palette.pal', 'wb+') as f:
        f.write(extract_palette(prg, 0xAD17))
    with open('skins/classic/legal/screen.nam', 'wb+') as f:
        f.write(extract_nametable(prg, 0xADB8))

    with open('skins/classic/level_menu/palette_a.pal', 'wb+') as f:
        # the original prg patches the highlight color
        palette = bytearray(extract_palette(prg, 0xAD2B))
        palette[10] = get_prg_range(prg, 0xC95D+3, 1)[0]
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

    # TODO: sfx???
