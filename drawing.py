from PIL import ImageTk, Image as PIL_Image, ImageDraw, ImageFont, ImageColor
from tkinter import *

from display_settings import DisplaySettings


def draw_landmarks(root, preview):
    sts: DisplaySettings = DisplaySettings()

    draw = ImageDraw.Draw(preview)

    sz = sts.landmarkFontSize
    font = ImageFont.truetype('font/Ubuntu-B.ttf', size=sz)
    lw = sts.connectionWidth

    for s in root.info_bar.listbox_landmarks.get(0, last=END):
        parts = tuple(s.split(','))
        _, code, r, color, x, y = parts
        r, x, y = tuple(map(int, (r, x, y)))

        for d in range(int(lw)):
            r1 = r + d
            draw.ellipse((x - r1, y - r1, x + r1, y + r1), outline=color)
            draw.text((x - sz // 4 * 3, y - sz // 2), code, font=font)


def draw_connections(root, preview):
    sts: DisplaySettings = DisplaySettings()

    draw = ImageDraw.Draw(preview)

    sz = sts.distanceFontSize
    font = ImageFont.truetype('font/Ubuntu-B.ttf', size=sz)
    lw = sts.connectionWidth

    for c in root.info_bar.listbox_connections.get(0, last=END):
        parts = tuple(c.split(','))
        code1, code2 = parts

        ls = []
        for s in root.info_bar.listbox_landmarks.get(0, last=END):
            parts = tuple(s.split(','))
            _, code, r, _, x, y = parts
            r, x, y = tuple(map(int, (r, x, y)))
            if code in [code1, code2]:
                ls.append((r, x, y))

        if len(ls) != 2:
            print(f'WARNING: failed with connection {c}, found {len(ls)} landmarks instead of 2')
        else:
            pass
