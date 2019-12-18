#!/usr/bin/python3

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv

line1 = ('1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927')
line2 = ('2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537')
satellite = twoline2rv(line1, line2, wgs72)
position, velocity = satellite.propagate(2019, 12, 18, 8, 30, 0)

from pprint import pprint
pprint(vars(satellite))
