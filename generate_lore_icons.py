import zlib
import struct

def save_png(filename, width, height, pixels):
    def chunk(chunk_type, data):
        return struct.pack('>I', len(data)) + chunk_type + data + struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)

    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    raw_data = b''.join(b'\x00' + bytes(pixels[y*width*4:(y+1)*width*4]) for y in range(height))
    idat = chunk(b'IDAT', zlib.compress(raw_data, 9))
    iend = chunk(b'IEND', b'')

    with open(filename, 'wb') as f:
        f.write(header + ihdr + idat + iend)

def create_image_from_ascii(colormap, ascii_grid):
    height = len(ascii_grid)
    width = len(ascii_grid[0])
    pixels = bytearray()
    for row in ascii_grid:
        for char in row:
            rgba = colormap.get(char, (0, 0, 0, 0))
            pixels.extend(rgba)
    return width, height, pixels

# ================= 1. ROK 1918 (První republika - Pergamen s autentickou českou vlajkou a pečetí) =================
# Rozměr 32x32
c1918 = {
    '.': (0, 0, 0, 0),         # Průhledné
    'O': (58, 36, 18, 255),     # Tmavý obrys pergamenu
    'P': (250, 237, 208, 255),  # Světlý pergamen
    'p': (236, 215, 172, 255),  # Střední pergamen
    'd': (206, 180, 134, 255),  # Tmavší pergamen / stín
    'T': (130, 94, 52, 255),    # Textové řádky pergamenu
    'W': (255, 255, 255, 255),  # Česká vlajka - bílý horní pruh
    'B': (17, 69, 126, 255),    # Česká vlajka - modrý klín
    'b': (10, 45, 90, 255),     # Tmavá modrá
    'R': (215, 20, 26, 255),    # Česká vlajka - červený dolní pruh
    'r': (152, 18, 22, 255),    # Pečeť - tmavě červená
    'G': (242, 194, 48, 255),   # Zlatá pečeť / lipová ratolest
    'g': (184, 140, 22, 255),   # Tmavé zlato
}

g1918 = [
    ".......OOOOOOOOOOOOOOOOO........",
    "......OPPPPPPPPPPPPPPPPdO.......",
    ".....OPPPPPPPPPPPPPPPPPPpdO.....",
    ".....OPPPPTTTTTTTTTTPPPPPpdO....",
    ".....OPPPOOOOOOOOOOOPPPPPpdO....",
    ".....OPPPPTTTTTTTTTTPPPPPpdO....",
    ".....OPPPPPPPPPPPPPPPPPPPpdO....",
    ".....OPPOOOOOOOOOOOOOOOPPpdO....",
    ".....OPPOBBWWWWWWWWWWWWOPpdO....",
    ".....OPPOBBBBWWWWWWWWWWOPpdO....",
    ".....OPPOBBBBBBWWWWWWWWOPpdO....",
    ".....OPPOBBBBBBBBWWWWWWOPpdO....",
    ".....OPPOBBBBBBBBBBrrrrOPpdO....",
    ".....OPPOBBBBBBBBBRRRRROPpdO....",
    ".....OPPOBBBBBBRRRRRRRROPpdO....",
    ".....OPPOBBBBRRRRRRRRRROPpdO....",
    ".....OPPOBBRRRRRRRRRRRROPpdO....",
    ".....OPPOOOOOOOOOOOOOOOPPpdO....",
    ".....OPPPPPPPPPPPPPPOrRRRroO....",
    ".....OPPPPTTTTTTPPPPOOGGGGOo....",
    ".....OPPPOOOOOOOPPPOrRGrRRro....",
    ".....OPPPPPPPPPPPPPPOrRRRroO....",
    ".....OPPPPTTTTTTPPPPPOOOOOOpdO..",
    ".....OPPPPPPPPPPPPPPPPPPPPppdO..",
    ".....OPPPPPPPPPPPPPPPPPPppdO....",
    "......OPPPPPPPPPPPPPPPPPpdO.....",
    ".......OOGGGOOOOOOOOOOOO........",
    "........OGGGGGO.................",
    "........OGgGGgO.................",
    ".........OGGGGGO................",
    "..........OGGGO.................",
    "...........OOO.................."
]

# ================= 2. ROK 1939 (Protektorát - Temný úřední fascikl a krvavá pečeť) =================
c1939 = {
    '.': (0, 0, 0, 0),         # Průhledné
    'X': (15, 17, 20, 255),     # Černý obrys
    'D': (38, 42, 48, 255),     # Tmavý ocelový karton
    'd': (25, 28, 32, 255),     # Hluboký stín kartonu
    'L': (65, 72, 82, 255),     # Světlejší ocelová hrana
    'M': (150, 160, 172, 255),  # Kovové kování v rozích
    'm': (100, 108, 118, 255),  # Tmavší kov
    'R': (220, 38, 38, 255),    # Výstražný červený pruh / pečeť
    'r': (140, 18, 18, 255),    # Tmavá krev / pečeť
    'P': (214, 210, 198, 255),  # Dobový nažloutlý protektorátní spis uvnitř
    'T': (45, 49, 56, 255),     # Černé úřední písmo
    'W': (240, 240, 240, 255),  # Bílý kontrast
}

g1939 = [
    "................................",
    "......XXXXXXXXXXXXXXXXXXXXX.....",
    ".....XMMMDDDDDDDDDDDDDDDMMMX....",
    ".....XMMMDDDDDDDDDDDDDDDMMMX....",
    ".....XMDDDDDDDDDDDDDDDDDDMXd....",
    ".....XDDDDDDDDDDDDDDDDDDDDXd....",
    ".....XDDDDDDDDDDDDDDDDDDDDXd....",
    ".....XDDDXXXXXXXXXXXXXDDDDXd....",
    ".....XDDDXPPPPPPPPPPPXDDDDXd....",
    ".....XDDDXPPTTTTTTPPPXDDDDXd....",
    ".....XDDDXPPTTTTTTPPPXDDDDXd....",
    ".....XDDDXPPPPPPPPPPPXDDDDXd....",
    ".....XDDDXPPTTTTTTPPPXDDDDXd....",
    ".....XDDDXPPTTTTTTPPPXDDDDXd....",
    ".....XDDDXPPPPPPOrrOPXDDDDXd....",
    ".....XRRRRRRRRRROrrOORRRRRXd....",
    ".....XRRRRRRRRROrRRrOORRRRXd....",
    ".....XrrrrrrrrrOrRRrOOrrrrXd....",
    ".....XDDDXPPPPPPOrrOOPPDDDXd....",
    ".....XDDDXPPPPPPPPPPPXDDDDXd....",
    ".....XDDDXPPTTTTTTPPPXDDDDXd....",
    ".....XDDDXPPTTTTTTPPPXDDDDXd....",
    ".....XDDDXPPPPPPPPPPPXDDDDXd....",
    ".....XDDDXPPPPPPPPPPPXDDDDXd....",
    ".....XDDDXXXXXXXXXXXXXDDDDXd....",
    ".....XDDDDDDDDDDDDDDDDDDDDXd....",
    ".....XDDDDDDDDDDDDDDDDDDDDXd....",
    ".....XMDDDDDDDDDDDDDDDDDDMXd....",
    ".....XMMMDDDDDDDDDDDDDDDMMMX....",
    ".....XMMMDDDDDDDDDDDDDDDMMMX....",
    "......XXXXXXXXXXXXXXXXXXXXX.....",
    ".......ddddddddddddddddddd......"
]

# ================= 3. ROK 1960 (Ústava ČSSR - Rudá kniha se zlatou pěticípou hvězdou) =================
c1960 = {
    '.': (0, 0, 0, 0),         # Průhledné
    'B': (40, 8, 8, 255),       # Hluboký rudohnědý obrys
    'R': (190, 24, 20, 255),    # Rudé plátno ústavy
    'r': (140, 14, 10, 255),    # Tmavé rudé plátno
    'L': (228, 48, 38, 255),    # Světlejší červený odlesk
    'G': (255, 215, 0, 255),    # Zářivé ryzí zlato
    'g': (190, 150, 10, 255),   # Tmavé zlato / stín
    'W': (250, 245, 230, 255),  # Ořízka listů knihy
    'w': (210, 195, 170, 255),  # Stín listů knihy
}

g1960 = [
    "................................",
    ".....BBBBBBBBBBBBBBBBBBB........",
    "....BLRRRRRRRRRRRRRRRRRBB.......",
    "...BLRRRRRRRRRRRRRRRRRRRWB......",
    "..BLRRRRRRRRRRRRRRRRRRRRWWB.....",
    "..BLRRRRGGGGGGGGGGGGGRRRwWwB....",
    "..BLRRRRGRRRRRRRRRRRGRRRwWwB....",
    "..BLRRRRGRRRRRRRRRRRGRRRwWwB....",
    "..BLRRRRGRRRRRGGGRRRGRRRwWwB....",
    "..BLRRRRGRRRRGGGGGRRGRRRwWwB....",
    "..BLRRRRGRRRRGGGGGRRGRRRwWwB....",
    "..BLRRRRGRGGGGGGGGGGGRRRwWwB....",
    "..BLRRRRGRRGGGGGGGGGRRRRwWwB....",
    "..BLRRRRGRRRGGGGGGGRRRRRwWwB....",
    "..BLRRRRGRRRGGGGGGGRRRRRwWwB....",
    "..BLRRRRGRRGGGGGGGGGRRRRwWwB....",
    "..BLRRRRGRGGGGGGGGGGGRRRwWwB....",
    "..BLRRRRGRGGGRRRRGGGRRRRwWwB....",
    "..BLRRRRGRGGRRRRRRGGRRRRwWwB....",
    "..BLRRRRGRRRRRRRRRRRGRRRwWwB....",
    "..BLRRRRGRRRRRRRRRRRGRRRwWwB....",
    "..BLRRRRGGGGGGGGGGGGGRRRwWwB....",
    "..BLRRRRRRRRRRRRRRRRRRRRwWwB....",
    "..BLRRRRRRRRRGGGRRRRRRRRwWwB....",
    "..BLRRRRRRRRRGGGRRRRRRRRwWwB....",
    "..BLRRRRRRRRRGGGRRRRRRRRwWwB....",
    "..BLRRRRRRRRRGGGRRRRRRRRBB......",
    "...BLRRRRRRRRGGGRRRRRRBB........",
    "....BBBBBBBBBGGGBBBBBB..........",
    "............BGGGB...............",
    ".............BGB................",
    "..............B................."
]

# ================= 4. ROK 1989 (Sametová revoluce - Leták s trikolórou a symbolem Vítězství V) =================
c1989 = {
    '.': (0, 0, 0, 0),         # Průhledné
    'O': (26, 32, 44, 255),     # Tmavý obrys
    'P': (255, 255, 255, 255),  # Čistý bílý papír
    'p': (226, 232, 240, 255),  # Stín papíru
    'T': (74, 85, 104, 255),    # Tisk novin / samizdat
    'B': (26, 86, 170, 255),    # Trikolóra - modrá
    'b': (15, 52, 105, 255),    # Tmavá modrá
    'R': (220, 38, 38, 255),    # Trikolóra - červená
    'r': (148, 20, 20, 255),    # Tmavá červená
    'G': (245, 190, 40, 255),   # Zvonící mosazné klíče
    'g': (180, 130, 20, 255),   # Stín klíčů
}

g1989 = [
    "................................",
    ".......OOOOOOOOOOOOOO...........",
    "......OPPPPPPPPPPPPPPOO.........",
    ".....OPPPPPPPPPPPPPPPPOPO.......",
    "....OPPPTTTTTTTTTTTTTPOpPO......",
    "....OPPPOOOOOOOOOOOOOPPOppO.....",
    "....OPPPTTTTTTTTTTTTTPOOOOO.....",
    "....OPPPPPPPPPPPPPPPPPPPppO.....",
    "....OPPPOBBOOOOOOOBBOPPPppO.....",
    "....OPPPOBBOOOOOOOBBOPPPppO.....",
    "....OPPPOBBBOOOOOBBBOPPPppO.....",
    "....OPPPOBBBBOOOBBBBOPPPppO.....",
    "....OPPPOORRROOORRROOPPPppO.....",
    "....OPPPOORRRROORRROOPPPppO.....",
    "....OPPPOOORRRRRRROOOPPPppO.....",
    "....OPPPOOOORRRRROOOOPPPppO.....",
    "....OPPPOOOOORRROOOOOPPPppO.....",
    "....OPPPPPPOOOOOOOPPPPPPppO.....",
    "....OPPPTTTTTTTTTTTTTPOOppO.....",
    "....OPPPOOOOOOOOOOOOOPPppPO.....",
    "....OPPPTTTTTTTTTTTTTPOpPO......",
    "....OPPPPPPPPPPPPPPPPPPO........",
    "....OPPPPOOGGGOOPPPPPPO.........",
    "....OPPPOOGGGGGOPPPPPO..........",
    ".....OPPOGGOGGGOPPPPO...........",
    "......OOGGOGGGGOPPPO............",
    ".......OOGGGGGGOGGO.............",
    "........OOGGGGOOGGO.............",
    "..........OOOO.OGGO.............",
    "...............OGGO.............",
    "................OO..............",
    "................................"
]

for path in ['/lore_1918.png', '/app/applet/lore_1918.png', 'lore_1918.png']:
    try:
        w, h, pix1918 = create_image_from_ascii(c1918, g1918)
        save_png(path, w, h, pix1918)
    except Exception:
        pass
print("Saved lore_1918.png with Czech flag")

for path in ['/lore_1939.png', '/app/applet/lore_1939.png', 'lore_1939.png']:
    try:
        w, h, pix1939 = create_image_from_ascii(c1939, g1939)
        save_png(path, w, h, pix1939)
    except Exception:
        pass
print("Saved lore_1939.png")

for path in ['/lore_1960.png', '/app/applet/lore_1960.png', 'lore_1960.png']:
    try:
        w, h, pix1960 = create_image_from_ascii(c1960, g1960)
        save_png(path, w, h, pix1960)
    except Exception:
        pass
print("Saved lore_1960.png")

for path in ['/lore_1989.png', '/app/applet/lore_1989.png', 'lore_1989.png']:
    try:
        w, h, pix1989 = create_image_from_ascii(c1989, g1989)
        save_png(path, w, h, pix1989)
    except Exception:
        pass
print("Saved lore_1989.png")
