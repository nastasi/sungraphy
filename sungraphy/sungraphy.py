#!/usr/bin/env python3
import sys
import os
import pytz
from pylab import *
from sunposition.sunposition import sunpos
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import colorsys

year_cur = 2020
elev_cur = 84

# from 4 to 21 (18 hours)
# 52 weeks
hours = 18
hour_start = 5
weeks = 52
week_start = 0

w_hour = 66
h_week = 30

thick = 1

# the house
lat = 44.298409
lon = 9.369913

# angolo muro lungo -31.5° (ref xy)
# wall_norm = 180.0 + 101.5
wall_norm_start_angle = 31.5

# TODO: improve to reduce red green and blue and increase yellow and azure
def hsv2rgb(h, s, v):
    # * 2 / 3 exclude violet and red roundtrip
    ret = colorsys.hsv_to_rgb(h * 2.0 / 3.0, s, v)
    return tuple(int(x * 255) for x in ret)

OL_COL = (40, 40, 40)
BG_COL = (0, 0, 0)
FG_COL = (255, 255, 255)

# wall_norm: angle from north
def sungraphy(filename, wall_norm):
    img = Image.new('RGB', ((w_hour + thick) * (hours + 1) + thick,
                            (h_week + thick) * (weeks + 1) + thick),
                    color = OL_COL)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 15)
    # d. text((10,10), "Hello World", fill=(255,255,0))

    for week in range(0, weeks):
        for hour in range(0, hours):

            date_in = "%s-%d %02d:00:00" % (year_cur, 1 + (week * 7),
                                            hour + hour_start)

            dt_in = datetime.strptime(date_in, '%Y-%j %H:%M:%S')
            local_tz = pytz.timezone('CET')
            dt_loc = local_tz.localize(dt_in)
            target_tz = pytz.timezone('UTC')
            dt = target_tz.normalize(dt_loc)


            az, zen, ra, dec = sunpos(dt, lat, lon, elev_cur)[:4] #discard RA, dec, H

            # print (hour + hour_start, week, ra, dec)

            wall_angle = az - wall_norm
            horizon_ang = 90.0 - zen

            if (zen > 90.0 or
                wall_angle < -90.0 or
                wall_angle > 90.0):
                d.rectangle([(thick + w_hour) * (hour + 1) + thick,
                             (h_week + thick) * (week + 1) + thick,
                             (thick + w_hour) * (hour + 2) - thick,
                             (h_week + thick) * (week + 2) - thick],
                            fill = BG_COL)
                continue

            # print (hour + hour_start, week, wall_angle, zen)
            d.rectangle([(thick + w_hour) * (hour + 1) + thick,
                         (h_week + thick) * (week + 1) + thick,
                         (thick + w_hour) * (hour + 2) - thick,
                         (h_week + thick) * (week + 2) - thick],
                        fill = BG_COL)
            d.rectangle([(thick + w_hour) * (hour + 1) + int(float(w_hour) * zen / 180.0) + thick,
                         (h_week + thick) * (week + 1) + thick,
                         (thick + w_hour) * (hour + 2)  - int(float(w_hour) * zen / 180.0) - thick,
                         (h_week + thick) * (week + 2) - thick],
                        fill = hsv2rgb((1.0 / 180.0) * (wall_angle + 90.0), 1, 1))

    hour = -1
    d.rectangle([(thick + w_hour) * (hour + 1) + thick,
                 (h_week + thick) * 0 + thick,
                 (thick + w_hour) * (hour + 2) - thick,
                 (h_week + thick) * 1 - thick],
                fill = BG_COL)

    for hour in range(0, hours):
        s = "%d" % (hour + hour_start)
        tw, th = d.textsize(s, font=font)

        d.rectangle([(thick + w_hour) * (hour + 1) + thick,
                     (h_week + thick) * 0 + thick,
                     (thick + w_hour) * (hour + 2) - thick,
                     (h_week + thick) * 1 - thick],
                    fill = BG_COL)

        tpos = ((thick + w_hour) * (hour + 1) + thick + int((w_hour - tw) / 2),
                int((h_week - th) / 2)  + thick);
        d.text(tpos,
               s, font=font, fill=FG_COL)

    for week in range(0, weeks):
        s = "%d°" % (week + 1)
        tw, th = d.textsize(s, font=font)

        d.rectangle([(thick + w_hour) * 0 + thick,
                     (h_week + thick) * (week + 1) + thick,
                     (thick + w_hour) * 1 - thick,
                     (h_week + thick) * (week + 2) - thick],
                    fill = BG_COL)

        tpos = (thick  + int((w_hour - tw) / 2),
                (h_week + thick) * (week + 1) + thick + int((h_week - th) / 2))
        d.text(tpos,
               s, font=font, fill=FG_COL)


    img.save(os.path.join('out', filename + '.png'))


#
#  MAIN
#
cardinal = ['north', 'east', 'south', 'west']
for i in range(0, 4):
    sungraphy(('lavagna%d_%s' % (i + 1, cardinal[i])), wall_norm_start_angle + float(i * 90.0))

