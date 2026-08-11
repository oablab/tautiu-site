#!/usr/bin/env python3
"""Crop a white-background app-icon screenshot to the icon's colored square.

Usage: python3 scripts/crop_icon.py <input.png> <output.png> [--max 512]

Scans for saturated (non-white, non-gray) pixels to find the icon's rounded
square — ignoring the soft gray drop shadow — then center-crops a square with
a small inset so every edge lands on icon color. Verifies edges after crop.
Output is written as RGB PNG at the source resolution; resize afterwards with
`sips -Z 512 <output.png>` if needed.
"""
import sys, zlib, struct


def decode(path):
    d = open(path, 'rb').read()
    pos = 8; idat = b''
    while pos < len(d):
        ln, typ = struct.unpack('>I4s', d[pos:pos+8])
        if typ == b'IHDR':
            w, h, bd, ct = struct.unpack('>IIBB', d[pos+8:pos+18])
        elif typ == b'IDAT':
            idat += d[pos+8:pos+8+ln]
        pos += 12 + ln
    if ct not in (2, 6):
        sys.exit(f"unsupported PNG color type {ct} (need RGB/RGBA 8-bit)")
    bpp = 3 if ct == 2 else 4
    raw = zlib.decompress(idat); stride = w * bpp
    out = bytearray(w * h * bpp); prev = bytearray(stride); p = 0
    for y in range(h):
        f = raw[p]; p += 1
        line = bytearray(raw[p:p+stride]); p += stride
        if f == 1:
            for i in range(bpp, stride): line[i] = (line[i] + line[i-bpp]) & 255
        elif f == 2:
            for i in range(stride): line[i] = (line[i] + prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                a = line[i-bpp] if i >= bpp else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(stride):
                a = line[i-bpp] if i >= bpp else 0
                b = prev[i]; c = prev[i-bpp] if i >= bpp else 0
                pa, pb, pc = abs(b-c), abs(a-c), abs(a+b-2*c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        out[y*stride:(y+1)*stride] = line; prev = line
    return out, w, h, bpp


def encode_rgb(px, w, h, path):
    stride = w * 3
    raw = b''.join(b'\x00' + bytes(px[y*stride:(y+1)*stride]) for y in range(h))
    def chunk(t, data):
        c = t + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(raw, 9))
    png += chunk(b'IEND', b'')
    open(path, 'wb').write(png)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 2:
        sys.exit(__doc__)
    src, dst = args
    px, w, h, bpp = decode(src)
    stride = w * bpp

    # bbox of "colored" pixels: saturated enough to be icon, not white/gray shadow
    minx, miny, maxx, maxy = w, h, 0, 0
    for y in range(h):
        row = px[y*stride:(y+1)*stride]
        for x in range(w):
            r, g, b = row[x*bpp:x*bpp+3]
            mx, mn = max(r, g, b), min(r, g, b)
            if mx - mn > 25 and mx > 60:  # saturated color, excludes white + gray shadow
                minx = min(minx, x); maxx = max(maxx, x)
                miny = min(miny, y); maxy = max(maxy, y)
    if maxx <= minx:
        sys.exit("no colored region found — is this a grayscale icon? adjust threshold")
    print(f"source {w}x{h}, colored bbox: ({minx},{miny})-({maxx},{maxy})")

    inset = max(2, (maxx - minx) // 80)
    x0, y0, x1, y1 = minx + inset, miny + inset, maxx - inset, maxy - inset
    side = min(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    x0, y0 = cx - side // 2, cy - side // 2
    x1, y1 = x0 + side, y0 + side
    print(f"crop: ({x0},{y0})-({x1},{y1}) side={side}")

    crop = bytearray(side * side * 3)
    for y in range(side):
        srow = px[(y0+y)*stride + x0*bpp : (y0+y)*stride + x1*bpp]
        if bpp == 4:
            drow = crop[y*side*3:(y+1)*side*3]
            for i in range(side):
                drow[i*3:i*3+3] = srow[i*4:i*4+3]
            crop[y*side*3:(y+1)*side*3] = drow
        else:
            crop[y*side*3:(y+1)*side*3] = srow
    encode_rgb(crop, side, side, dst)

    # verify edge midpoints are not white
    px2, w2, h2, _ = decode(dst)
    bad = []
    for name, (x, y) in {"top": (w2//2, 0), "bottom": (w2//2, h2-1),
                         "left": (0, h2//2), "right": (w2-1, h2//2)}.items():
        i = (y*w2 + x) * 3
        r, g, b = px2[i:i+3]
        white = r > 240 and g > 240 and b > 240
        print(f"  {name} edge rgb=({r},{g},{b}) {'WHITE!' if white else 'ok'}")
        if white:
            bad.append(name)
    if bad:
        sys.exit(f"FAIL: white on {bad}")
    print("ALL EDGES CLEAN ->", dst)


if __name__ == "__main__":
    main()
