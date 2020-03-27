#!/usr/bin/env python3

from perylune.OrbCalc import *
import numpy as np
from math import *

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

    def load(self, fname, clean = True):
        """This loads the file. Expected syntax: one or more lines, each line with the
           following syntax: name, x, y, z
           This should define one or more sats with their ECEF positions"""
        if clean:
            self.sats.clear()

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

    def objectsSubset(self, subset, objects):
        """This returns a subset (defined as array, e.g. [1,2,3,8]) of the objects"""
        result=[]
        for i in subset:
            result.append(objects[i])
        return result

    def printLoadedObjects(self, objects = None):
        '''Prints information about all loaded objects (sats, planets, asteroids etc.)'''
        if objects is None:
            objects = self.sats
        print("Loaded %d objects (sats, planets, asteroids, etc.)" % len(objects))
        i = 0
        for s in objects:
            print("%d: %s" % (i, s.getText()))
            i = i + 1

    def getObjectsECEFvectors(self, sats = None):
        ''' Returns xECEF, yECEF, zECEF of all loaded objects as vectors'''

        if sats is None:
            sats = self.sats

        xECEF = []
        yECEF = []
        zECEF = []

        for s in sats:
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

    def calculateAzimuth(self, xENU, yENU):

        AZ = np.zeros(xENU.shape[0])

        for i in range(0, xENU.shape[0]):
            if xENU[i] == 0 and yENU[i] > 0:
                AZ[i] = 0

            elif xENU[i] > 0 and yENU[i] > 0:
                AZ[i] = atan(abs(xENU[i]/yENU[i]))

            elif xENU[i] > 0 and yENU[i] == 0:
                AZ[i] = pi/2

            elif xENU[i] > 0 and yENU[i] < 0:
                AZ[i] = pi/2 + atan(abs(yENU[i]/xENU[i]))

            elif xENU[i] == 0 and yENU[i] < 0:
                AZ[i] = pi

            elif xENU[i] < 0 and yENU[i] < 0:
                AZ[i] = pi + atan(abs(xENU[i]/yENU[i]))

            elif xENU[i] < 0 and yENU[i] == 0:
                AZ[i] = 3*pi/2

            elif xENU[i] < 0 and yENU[i] > 0:
                AZ[i] = 3*pi/2 + atan(abs(yENU[i]/xENU[i]))
            else:
                raise Exception("Can't calculate azimuth: i=%d xENU[%d]=%f yENU[%d]=%f" % (i, i, xENU[i], i, yENU[i]))

        return AZ

    def calculateTopoHeight(self, xENU, yENU, zENU):
        HT = np.zeros(xENU.shape[0])

        for i in range(0, xENU.shape[0]):

            HT[i] = atan(zENU[i]/sqrt(xENU[i]*xENU[i] + yENU[i]*yENU[i]))

        return HT

    def method2calculateG(self, AZ, HT):
        G = np.zeros((AZ.shape[0], 4))
        for i in range(0, AZ.shape[0]):

            G[i][0]=cos(HT[i])*sin(AZ[i])
            G[i][1]=cos(HT[i])*cos(AZ[i])
            G[i][2]=sin(HT[i])
            G[i][3]=1

        return G

    def method2calculateA(self, G):

        # G^T * G
        tmp1 = np.dot(G.transpose(),G)

        # (G^T * G)^-1
        # Note: This may throw numpy.linalg.LinAlgError if the matrix is singular
        # (i.e. is not reversible)
        tmp2 = np.linalg.inv(tmp1)

        return tmp2

    def method2calculateDOP(self, A):
        '''Returns DOP parameters based on A matrix. Returned DOP parameters
           GDOP, PDOP, HDOP, VDOP, TDOP'''
        gdop = sqrt(A[0,0] + A[1,1] + A[2,2] + A[3,3])
        pdop = sqrt(A[0,0] + A[1,1] + A[2,2])
        hdop = sqrt(A[0,0] + A[1,1])
        vdop = sqrt(A[2,2])
        tdop = sqrt(A[3,3])
        return gdop, pdop, hdop, vdop, tdop

    def method2(self, obs_lla, obs_ecef, obj_ecef):
        '''Calculates DOP parameters using method 2. Three parameters need
           to be specified:
           - obs_lla - observer coordinates in long/lat/altitude
           - obs_ecef - observer coordinates in Earth Centered Earth Fixed
           - obj_ecef - objects (satelittes) in ECEF coords

           Returns a tuple of 5 DOP parameters:
           GDOP, PDOP, HDOP, VDOP, TDOP'''
        xENU, yENU, zENU = self.coordsECEFtoENU(obs_lla, obs_ecef, obj_ecef)

        AZ = self.calculateAzimuth(xENU, yENU)
        HT = self.calculateTopoHeight(xENU, yENU, zENU)

        G = self.method2calculateG(AZ,HT)
        #print("G=\n%s" % G)

        try:
            A = self.method2calculateA(G)
            #print("A=\n%s" % A)
        except np.linalg.LinAlgError:
            print("Unable to invert A matrix")
            return np.array([999, 999, 999, 999, 999])

        try:
            dops = self.method2calculateDOP(A)
        except ValueError:
            print("Unable to calculate DOP params. Primary A values negative")
            return np.array([998, 998, 998, 998, 998])

        return dops
