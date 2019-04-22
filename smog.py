#!/usr/bin/env python3

from OrbCalc import *

# GEO = 35786
# 880km = 14 orbit/dobe
# 554,25km = 15 orbit/dobe
a = 880000 + OrbCalc.getConst('earth-radius')

G = OrbCalc.getConst('G')
M = OrbCalc.getConst('M')

T = OrbCalc.getPeriod(a)
print("Okres dla orbity kolowej %f [km] wynosi %f [s]" % (a/1000, T))

day = OrbCalc.getConst('sidereal-day')

print("Dlugosc doby gwiazdowej = %f [s]" % OrbCalc.getConst('sidereal-day'))

print("%f orbit/dobe" % (day/T))

print("Predkosc ucieczki dla Ziemi = %f [m/s]" % OrbCalc.escapeVel())

