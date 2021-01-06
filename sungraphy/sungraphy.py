#!/usr/bin/env python3
from pylab import *
from sunposition.sunposition import sunpos
from datetime import datetime
from PIL import Image, ImageDraw
import colorsys
import os

year_cur = 2020
elev_cur = 84

# from 4 to 21 (18 hours)
# 52 weeks
hours = 18
hour_start = 3
weeks = 52
week_start = 0

h_hour = 66
w_week = 30

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

# wall_norm: angle from north
def sungraphy(filename, wall_norm):
    img = Image. new('RGB', ((w_week + thick) * weeks + thick,
                             (h_hour + thick) * hours + thick),
                     color = (0, 0, 0))
    d = ImageDraw.Draw(img)
    # d. text((10,10), "Hello World", fill=(255,255,0))
    for week in range(0, weeks):
        for hour in range(0, hours):

            date_in = "%s-%d %02d:00:00" % (year_cur, 1 + (week * 7),
                                            hour + hour_start)

            dt = datetime.strptime(date_in, '%Y-%j %H:%M:%S')

            az, zen, ra, dec = sunpos(dt, lat, lon, elev_cur)[:4] #discard RA, dec, H

            # print (hour + hour_start, week, ra, dec)

            wall_angle = az - wall_norm
            horizon_ang = 90.0 - zen

            if (zen > 90.0 or
                wall_angle < -90.0 or
                wall_angle > 90.0):
                d.rectangle([(w_week + thick) * week + thick,
                             (thick + h_hour) * hour + thick,
                             (w_week + thick) * (week + 1) - thick,
                             (thick + h_hour) * (hour + 1) - thick],
                            fill = (30, 30, 30))
                continue

            # print (hour + hour_start, week, wall_angle, zen)
            d.rectangle([(w_week + thick) * week + thick,
                         (thick + h_hour) * hour + thick,
                         (w_week + thick) * (week + 1) - thick,
                         (thick + h_hour) * (hour + 1) - thick],
                        fill = (30, 30, 30))
            d.rectangle([(w_week + thick) * week + thick,
                         (thick + h_hour) * hour + int(float(h_hour) * zen / 180.0) + thick,
    #                     (thick + h_hour) * hour + thick,
                         (w_week + thick) * (week + 1) - thick,
                         (thick + h_hour) * (hour + 1)  - int(float(h_hour) * zen / 180.0) - thick],
    #                     (thick + h_hour) * (hour + 1) - thick],
                        fill = hsv2rgb((1.0 / 180.0) * (wall_angle + 90.0), 1, 1))
            #           fill = hsv2rgb((1.0 / weeks) * week, 1, 1))

    img.save(os.path.join('out', filename + '.png'))


#
#  MAIN
#
cardinal = ['north', 'east', 'south', 'west']
for i in range(0, 4):
    sungraphy('lavagna_' + cardinal[i], wall_norm_start_angle + float(i * 90.0))
    
    
# # evaluate on a 2 degree grid
# lon = linspace(-180, 180, 181)
# lat = linspace(-90, 90, 91)
# LON, LAT = meshgrid(lon,lat)
# #at the current time
# now = datetime.utcnow()
# az,zen = sunpos(now,LAT,LON,0)[:2] #discard RA, dec, H
# print(az, zen)
# # #convert zenith to elevation
# # elev = 90 - zen
# # #convert azimuth to vectors
# # u, v = cos((90-az)*pi/180), sin((90-az)*pi/180)
# # #plot
# # figure()
# # imshow(elev,cmap=cm.CMRmap,origin='lower',vmin=-90,vmax=90,extent=(-180,180,-90,90))
# # s = slice(5,-1,5) # equivalent to 5:-1:5
# # quiver(lon[s],lat[s],u[s,s],v[s,s])
# # contour(lon,lat,elev,[0])
# # cb = colorbar()
# # cb.set_label('Elevation Angle (deg)')
# # gca().set_aspect('equal')
# # xticks(arange(-180,181,45)); yticks(arange(-90,91,45))
