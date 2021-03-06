import math
from PIL import ImageDraw, ImageFont
from tkinter import *

from display_settings import DisplaySettings


def draw_landmarks(root, preview):
    sts: DisplaySettings = DisplaySettings()

    draw = ImageDraw.Draw(preview)

    sz = sts.landmarkFontSize
    font = ImageFont.truetype(sts.font_path, size=sz)
    lw = sts.connectionWidth

    for s in root.info_bar.listbox_landmarks.get(0, last=END):
        parts = tuple(s.split(','))
        _, code, r, color, x, y = parts
        r, x, y = tuple(map(int, (r, x, y)))

        for d in range(int(lw)):
            r1 = r + d
            draw.ellipse((x - r1, y - r1, x + r1, y + r1), outline=color)
            r1 += 0.5
            draw.ellipse((x - r1, y - r1, x + r1, y + r1), outline=color)

        tw, th = draw.textsize(code, font=font)
        draw.text((x - tw // 2, y - th // 2), code, font=font)


def draw_connections(root, preview):
    sts: DisplaySettings = DisplaySettings()

    draw = ImageDraw.Draw(preview)

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
            draw_connection_line(draw, ls, sts)
            if root.info_bar.draw_distances.get():
                draw_distance_text(draw, ls, root, sts)
            if root.info_bar.draw_angles.get():
                draw_connection_angle(draw, ls, sts)
                draw_connection_angle(draw, ls[::-1], sts)


def draw_slides(root, preview):
    sts: DisplaySettings = DisplaySettings()
    draw = ImageDraw.Draw(preview)

    sh = root.info_bar.slide_height.get()
    sw = int(sh / 1.5)
    centers = root.info_bar.slide_centers

    for center_xy in centers:
        draw.rectangle((center_xy[0] - sw // 2, center_xy[1] - sh // 2, center_xy[0] + sw // 2, center_xy[1] + sh // 2),
                       fill=None, outline=sts.slidesColor)


def draw_distance_text(draw, ls, root, sts):
    sz = sts.distanceFontSize
    font = ImageFont.truetype(sts.font_path, size=sz)
    r1, x01, y01 = ls[0]
    r2, x02, y02 = ls[1]
    d0 = ((x01 - x02) ** 2 + (y01 - y02) ** 2) ** 0.5

    kilometers_per_nautical_mile = 1.852
    distance_km = round(d0 * root.info_bar.scale_kilometers_per_pixel.get())
    distance_nm = round(distance_km / kilometers_per_nautical_mile)
    clr = sts.connectionColor

    w = sts.distanceRectangleWidth
    h = sts.distanceRectangleHeight
    if distance_km > sts.minConnCenterDistKm:
        center_x = (x01 + x02) / 2.
        center_y = (y01 + y02) / 2.
        draw.rectangle((center_x - w // 2, center_y - h // 2, center_x + w // 2, center_y + h // 2), fill=clr)

        dist_text = '%i km\n%i nm' % (distance_km, distance_nm)
        tw, th = draw.textsize(dist_text, font=font)
        draw.text((center_x - tw // 2, center_y - th // 2), dist_text, font=font)


def draw_connection_line(draw, ls, sts):
    clr = sts.connectionColor
    dl = sts.connectionMargin
    lw = sts.connectionWidth

    r1, x01, y01 = ls[0]
    r2, x02, y02 = ls[1]
    d0 = ((x01 - x02) ** 2 + (y01 - y02) ** 2) ** 0.5
    x1 = x01 + (x02 - x01) * (r1 * sts.radiusMultiplier + dl) / d0
    y1 = y01 + (y02 - y01) * (r1 * sts.radiusMultiplier + dl) / d0
    x2 = x02 + (x01 - x02) * (r2 * sts.radiusMultiplier + dl) / d0
    y2 = y02 + (y01 - y02) * (r2 * sts.radiusMultiplier + dl) / d0
    draw.line([(x1, y1), (x2, y2)], fill=clr, width=lw)


def draw_connection_angle(draw, ls, sts):
    dl = sts.connectionMargin
    r1, x01, y01 = ls[0]
    r2, x02, y02 = ls[1]
    d0 = ((x01 - x02) ** 2 + (y01 - y02) ** 2) ** 0.5
    x1 = x01 + (x02 - x01) * (r1 * sts.radiusMultiplier + dl) / d0
    y1 = y01 + (y02 - y01) * (r1 * sts.radiusMultiplier + dl) / d0
    x2 = x02 + (x01 - x02) * (r2 * sts.radiusMultiplier + dl) / d0
    y2 = y02 + (y01 - y02) * (r2 * sts.radiusMultiplier + dl) / d0

    sz = sts.distanceFontSize
    font = ImageFont.truetype(sts.font_path, size=sz)
    color = sts.connectionColor
    w = sts.angleRectangleWidth
    h = sts.angleRectangleHeight
    degrees_in_radian = 57.295

    x1a = x1 + (x2 - x1) * w / 2 / d0
    y1a = y1 + (y2 - y1) * w / 2 / d0

    draw.rectangle((x1a - w // 2, y1a - h // 2, x1a + w // 2, y1a + h // 2), fill=color)

    angle = round(degrees_in_radian * math.atan2(x2 - x1, -(y2 - y1)))
    if angle < 0:
        angle = 360 + angle

    angle_text = '%i°' % angle
    tw, th = draw.textsize(angle_text, font=font)
    draw.text((x1a - tw // 2, y1a - th // 2), angle_text, font=font)
