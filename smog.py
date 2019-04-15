#!/usr/bin/env python3

from OrbCalc import *

a = 35786000 + OrbCalc.getConst('earth-radius')

G = OrbCalc.getConst('G')
M = OrbCalc.getConst('M')

print("Okres dla orbity kolowej %f [km] wynosi %f [s]" % (a/1000, OrbCalc.getPeriod(a)))

print("Dlugosc doby gwiazdowej = %f [s]" % OrbCalc.getConst('sidereal-day'))

print("Predkosc ucieczki dla Ziemi = %f [m/s]" % OrbCalc.escapeVel())

