#!/usr/bin/env python3
"""Generate the OG card for the DeepSRT Transcribe landing page.

Uses the app icon palette: deep olive gradient, app icon + name top-left,
big white headline, muted sub-line, accent domain bottom-left, and a huge
translucent glyph bleeding off the right edge. 1200x630, the standard OG size.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
# Deep olive sampled from the app icon, slightly lighter toward the right.
TOP_LEFT = (38, 45, 31)
BOTTOM_RIGHT = (80, 89, 57)
WHITE = (255, 250, 242)
MUTED = (218, 220, 200)
ACCENT = (190, 201, 148)
WATERMARK = (62, 70, 45)

# PingFang.ttc no longer loads in Pillow on macOS 26 ("cannot open resource"),
# so the TC face is Heiti TC Medium; SF Mono for the domain line, matching the
# reference card's monospaced deepsrt.com.
HEITI_TC = "/System/Library/Fonts/STHeiti Medium.ttc"   # index 0 = Heiti TC
SF = "/System/Library/Fonts/SFNS.ttf"
SF_MONO = "/System/Library/Fonts/SFNSMono.ttf"


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def gradient(draw):
    for y in range(H):
        t = y / H
        row = tuple(int(TOP_LEFT[i] + (BOTTOM_RIGHT[i] - TOP_LEFT[i]) * t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=row)


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw)

    # Watermark: giant D bleeding off the right, like the original.
    wm_font = font(SF, 560)
    draw.text((W - 190, H // 2 + 40), "D", font=wm_font, fill=WATERMARK, anchor="mm")

    # App icon + name, top left (icon has its own squircle + transparency).
    icon = Image.open("assets/deepsrt-transcribe.png").convert("RGBA").resize((88, 88), Image.LANCZOS)
    img.paste(icon, (72, 60), icon)
    draw.text((180, 104), "DeepSRT Transcribe", font=font(SF, 42), fill=WHITE, anchor="lm")

    # Headline, two lines — mirrors the note card's layout.
    head = font(HEITI_TC, 72)
    draw.text((72, 290), "把影片拖進來", font=head, fill=WHITE, anchor="lm")
    draw.text((72, 380), "瞬間幫你上好繁中字幕", font=head, fill=WHITE, anchor="lm")

    # Sub-line, muted — the tag line under the headline in the reference.
    sub = font(HEITI_TC, 30)
    draw.text((72, 470), "本地運算不用上傳 · Gemini 優化語言 · Google 搜尋自動校正", font=sub, fill=MUTED, anchor="lm")

    # Domain, accent, monospaced, bottom left.
    draw.text((72, 572), "tautiu.dev/deepsrt-transcribe", font=font(SF_MONO, 26), fill=ACCENT, anchor="lm")

    img.save("assets/deepsrt-transcribe-og.png", "PNG", optimize=True)
    print("wrote assets/deepsrt-transcribe-og.png", img.size)


if __name__ == "__main__":
    main()
