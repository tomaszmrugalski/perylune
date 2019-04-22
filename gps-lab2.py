#!/usr/bin/env python3

from OrbCalc import *
import numpy as np

class CoordsECEF:
    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self, name, x, y, z):
        self.name = name.strip()
        self.x = float(str(x).strip())
        self.y = float(str(y).strip())
        self.z = float(str(z).strip())

    def getText(self):
        return "%s: ECEF=%f,%f,%f" % (self.name, self.x, self.y, self.z)

class GpsDop:

    sats = []

    def load(self, fname):
        try:
            sat = None
            for line in open(fname,'r').readlines():

                # skip empty lines
                if not len(line):
                    continue

                # skip comments (starting with one of # ; %)
                if line[0] in ['#', ';', '%']:
                    continue
                
                name, x, y, z = line.split(',')

                coords = CoordsECEF(name, x, y, z)
                
                self.sats.append(coords)

        except IOError:
            print("Failed to open %s file" % fname)

    def printLoadedObjects(self):
        '''Prints information about all loaded objects (sats, planets, asteroids etc.)'''
        print("Loaded %d objects (sats, planets, asteroids, etc.)" % len(self.sats))
        i = 0
        for s in self.sats:
            print("%d: %s" % (i, s.getText()))
            i = i + 1

    def getObjectsECEFvectors(self):
        ''' Returns xECEF, yECEF, zECEF of all loaded objects as vectors'''
        xECEF = []
        yECEF = []
        zECEF = []

        for s in self.sats:
            xECEF.append(s.x)
            yECEF.append(s.y)
            zECEF.append(s.z)

        return np.array(xECEF), np.array(yECEF), np.array(zECEF)

    def getObserverECEF(self, x = OrbCalc.getConst("earth-radius"), y = 0, z = 0):
        '''Returns observer coords in ECEF system. If not specified otherwise
           the values returned are for 0N 0E at the altitude of 0 meters above spheroid'''
        return np.array([x, y, z])

    def getObserverLLA(self, B = 0.0, L = 0.0, h = 0.0):
        '''Returns observer coords in LLA system. B (topocentric latitude) and 
           L (topocentric longitute) are expressed in radians, h expressed in meters
           above spheroid.'''
        return np.array([B, L, h])

    def coordsECEFtoENU(self, obs_lla, obs_ecef, obj_ecef):
        '''Calculates ENU (East, North, Up) for specified objects (coords specified in ECEF)
           for an observator (observator coords specified in LLA and ECEF).
           Returns a tuple of 3 vectors: xENU, yENU, zENU'''
        B = obs_lla[0]
        L = obs_lla[1]
        h = obs_lla[2]

        # F is a transformation matrix
        F = np.array([ [ -sin(L),         cos(L),        0      ],
                       [ -sin(B)*cos(L), -sin(B)*sin(L), cos(B) ],
                       [ cos(B)*cos(L),   cos(B)*sin(L), sin(B) ] ])

        vec_x = obj_ecef[0] - obs_ecef[0]
        vec_y = obj_ecef[1] - obs_ecef[1]
        vec_z = obj_ecef[2] - obs_ecef[2]

        xENU = np.zeros(obj_ecef[0].shape)
        yENU = np.zeros(obj_ecef[0].shape)
        zENU = np.zeros(obj_ecef[0].shape)
        
        for i in range(0, obj_ecef[0].shape[0]):
            tmp = np.array([ vec_x[i], vec_y[i], vec_z[i]])
            result = np.dot(F,tmp)
            xENU[i] = result[0]
            yENU[i] = result[1]
            zENU[i] = result[2]

        return xENU, yENU, zENU

gps = GpsDop()

gps.load("data/gps-lab2-ecef-coords.txt")
# gps.printLoadedObjects()

obj_ecef = gps.getObjectsECEFvectors()
obs_ecef = gps.getObserverECEF()
obs_lla  = gps.getObserverLLA()

xENU, yENU, zENU = gps.coordsECEFtoENU(obs_lla, obs_ecef, obj_ecef)

print("xENU=%s" % xENU)
print("yENU=%s" % yENU)
print("zENU=%s" % zENU)




#print("--------------")
#A = np.array([ [1, 2, 3], [4, 5, 6], [7, 8, 9] ])
#V = np.array([ 1, 3, 5])
#print(A)
#print(V)
#print(np.dot(A, V))
