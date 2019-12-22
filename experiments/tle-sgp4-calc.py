#!/usr/bin/python3

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv


# ISS
line1 = ('1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927')
line2 = ('2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537')

# NOAA-15
line1 = ('1 25338U 98030A   19351.71640046 +.00000015 +00000-0 +24973-4 0  9993')
line2 = ('2 25338 098.7340 012.5392 0011411 075.8229 284.4218 14.25943731122932')

satellite = twoline2rv(line1, line2, wgs72)
position, velocity = satellite.propagate(2019, 12, 18, 0, 0, 0)

# from pprint import pprint
# pprint(vars(satellite))

year = 2019
month = 12
day = 19

h = 0
m = 0
s = 0

print("    \"cartesian\":[")

for t in range(0, 86400 + 300, 300):
    h = int(t / 3600)
    m = int( (t - 3600*h)/60)
    s = t - 3600*h - 60*m
    position, velocity = satellite.propagate(year, month, day, h, m, s)
    print("    %d,%f,%f,%f," % (t, position[0]*1000, position[1]*1000, position[2]*1000))

print("    ]")
