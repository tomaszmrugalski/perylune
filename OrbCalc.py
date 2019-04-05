# The OrbCalc library is dedicated to calculating various parameters
# related to kerplerian orbits. It is very modest now, but it is
# expected to grow in capacity.

import string
import math

class OrbCalc:

    '''This defines various constants'''
    CONSTS = {
         'earth-radius' :    [ 6378137,          'm', 'Description here' ],
         'earth-flattening': [ 0.00335281068118, '', 'Earth flattening' ],
         'rho':              [ 180.0/math.pi,    '', 'Used to convert degrees to radians']
        }

    def parseLongitude(text):

        # get rid of the whitespaces first
        text = text.strip()

        text = text.replace(',' , '.')

        if not len(text):
            # If the string is empty, assume 0
            tmp = [ 0 ]
        else:
            # If non-empty, split into up to 3 elements
            tmp = text.split(" ", 3)

        # If it's too short (e.g. only degrees defined, add 0 minutes)
        if (len(tmp) < 3):
            tmp.append(0)

        # Do the same for unspecified seconds
        if (len(tmp) < 3):
            tmp.append(0)

        values = [ int(tmp[0]), int(tmp[1]), float(tmp[2]) ]

        # print("[%d %d %f]" % (values[0], values[1], values[2]))

        return values

    # This assumes l is an array of 3 integer/float values)
    def longitudeToFloat(l):
        x = l[0] + float(l[1])/60 + float(l[2])/3600
        return x

    def deg2rad(d):
        return d*math.pi/180

    def rad2deg(r):
        return r*180/math.pi

    def getRho():
        '''Returns rho (used to convert degrees to radians)'''
        return 180.0/math.pi

    def getEarthRadius():
        '''Returns earth diameter in meters'''
        return OrbCalc.CONSTS['earth-radius'][0]

    def getConst(name):
        '''Returns constant of specified name'''
        return OrbCalc.CONSTS[name][0]

    def getConstUnits(name):
        return OrbCalc.CONSTS[name][1]

    def getConstDescr(name):
        return OrbCalc.CONSTS[name][2]
