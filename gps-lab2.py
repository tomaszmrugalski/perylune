#!/usr/bin/env python3

from GpsDop import *

gps = GpsDop()

# Wczytaj dane 10 satelitow z pliku
gps.load("data/gps-lab2-ecef-coords.txt")

obj_ecef = gps.getObjectsECEFvectors()
obs_ecef = gps.getObserverECEF()
obs_lla  = gps.getObserverLLA()

print("Using following satellites:")
gps.printLoadedObjects()

dops2 = gps.method2(obs_lla, obs_ecef, obj_ecef)
print("DOP params: GDOP, PDOP, HDOP, VDOP, TDOP")
print(dops2)
