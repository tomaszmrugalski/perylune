#!/usr/bin/env python3

from perylune.orbcalc import OrbCalc

# GEO = 35786 km
# 880km = 14 orbit/dobe
# 554,25km = 15 orbit/dobe

print("=== orbit 1: LEO (880km) ===")

a = 880000 + OrbCalc.getConst('earth-radius')

G = OrbCalc.getConst('G')
M = OrbCalc.getConst('M')

T = OrbCalc.getPeriod(a)
print("Period of a circular orbit of radius %f [km] is %f [s]" % (a/1000, T))

day = OrbCalc.getConst('sidereal-day')

print("Sidereal day (dlugosc doby gwiazdowej) = %f [s]" % OrbCalc.getConst('sidereal-day'))

print("Escape velocity for Earth (predkosc ucieczki dla Ziemi) = %f [m/s]" % OrbCalc.escapeVel())

print("=== orbit 2: GEO (35786) ===")

a = 42164 * 1000
T = OrbCalc.getPeriod(a)
print("Period of a circular orbit of radius %f [km] is %f [s]" % (a/1000, T))

print("%f orbits/sidereal day" % (day/T))

alt = a - OrbCalc.getConst('earth-radius')

print("GEO altitude (Wysokosc orbity GEO) is %f [km]" % (alt / 1000.0))
