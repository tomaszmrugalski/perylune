#!/usr/bin/env python3

from perylune.GpsDop import *

def combinations(n,max):

    combs = []
    cnt = 0
    for i in range(0,max):
        for j in range(i+1,max):
            for k in range(j+1, max):
                for l in range(k+1,max):
                    combs.append([i, j, k, l])
                    cnt = cnt + 1
    return combs

gps = GpsDop()

# Wczytaj dane 10 satelitow z pliku
gps.load("data/gps-lab2-ecef-coords.txt")

# Zainicjalizuj wspolrzedne obserwatora (w ukladzie ECEF i LLA)
obs_ecef = gps.getObserverECEF()
obs_lla  = gps.getObserverLLA()

# Wygeneruj wszystkie 4 elementowe kombinacje sposrod liczb 0..9
combs = combinations(4, len(gps.sats))

# Wypisz naglowek
print("Number, sat1,sat2,sat3,sat4,GDOP, PDOP, HDOP, VDOP, TDOP")

cnt = 0

for c in combs:

    # Wygeneruj z gps.sat (wszystkie 10 satelit) liste 4 satelit
    sats = gps.objectsSubset(c, gps.sats)

    # Policz wspolrzedne ECEF dla tych 4 satelit
    sats_ecef = gps.getObjectsECEFvectors(sats)

    # Oblicz wspolczynniki DOPS dla tych 4 satelit
    dops = gps.method2(obs_lla, obs_ecef, sats_ecef)

    # Wypisz wartosci
    print("%d, %d,%d,%d,%d,  %f, %f, %f, %f, %f" % (cnt, c[0], c[1], c[2], c[3], dops[0], dops[1], dops[2], dops[3], dops[4]))
    cnt += 1

