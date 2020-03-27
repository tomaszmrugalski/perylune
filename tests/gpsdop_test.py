# OrbCalc_test.py

from perylune.gpsdop import GpsDop
from perylune.orbcalc import OrbCalc

import numpy as np

import pytest

def test_getObserverECEF():
    gps = GpsDop()
    obs_ecef = gps.getObserverECEF()
    assert isinstance(obs_ecef, np.ndarray)

    # By default, Observer ECEF position is (earth-radius, 0 deg, 0 deg)
    assert obs_ecef[0] == OrbCalc.getConst('earth-radius')
    assert obs_ecef[1] == 0
    assert obs_ecef[2] == 0

    # TODO: Implement a test that uses non-standard ECEF coordinates

def test_getObserverLLA():
    gps = GpsDop()
    obs_lla = gps.getObserverLLA()
    assert isinstance(obs_lla, np.ndarray)
    assert obs_lla[0] == 0.0
    assert obs_lla[1] == 0.0
    assert obs_lla[2] == 0.0

def test_DopCalculation():

    # Load the sats, make sure there's exactly 10 of them.
    gps = GpsDop()
    gps.load("data/gps-lab2-ecef-coords.txt")
    assert len(gps.sats) == 10

    # Get observer position in both ECEF and LLA coordinate systems
    obs_ecef = gps.getObserverECEF()
    obs_lla  = gps.getObserverLLA()

    # We want the first 4 sats
    first4 = [0,1,2,3]
    # This returns 4 GpsDop.CoordsECEF objects.
    sats = gps.objectsSubset(first4, gps.sats)
    assert len(sats) == 4

    # Calculate ECEF positions for those 4 sats. This returns 3 vectors,
    # each vector having the length equal to the number of sats.
    sats_ecef = gps.getObjectsECEFvectors(sats)
    assert len(sats_ecef) == 3
    assert len(sats_ecef[0]) == 4
    assert len(sats_ecef[1]) == 4
    assert len(sats_ecef[2]) == 4

    # This returns five parameters: GDOP, PDOP, HDOP, VDOP, TDOP. The exact values for sats 0,1,2,3 are:
    # (5.802540612754398, 5.314511431088559, 3.2443396269879066, 4.209310173404538, 2.3292586398880695)
    dops2 = gps.method2(obs_lla, obs_ecef, sats_ecef)
    assert len(dops2) == 5
    assert abs(dops2[0] - 5.802540612754398) < 0.00001
    assert abs(dops2[1] - 5.314511431088559) < 0.00001
    assert abs(dops2[2] - 3.2443396269879066) < 0.00001
    assert abs(dops2[3] - 4.209310173404538) < 0.00001
    assert abs(dops2[4] - 2.3292586398880695) < 0.00001

def test_DopCalculation_many():
    """This test calculates DOP parameters for all 4 sat groups out of available 10.
       It doesn't test much. It's more like a demo."""

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

    # Load 10 sats positions from a file.
    gps.load("data/gps-lab2-ecef-coords.txt")
    assert len(gps.sats) == 10

    # Initiate the observer position (in both ECEF and LLA coordinate systems)
    obs_ecef = gps.getObserverECEF()
    obs_lla  = gps.getObserverLLA()

    # Generate all 4 element combination of those sats
    combs = combinations(4, len(gps.sats))
    print("len(gps.sats)= %d" % len(gps.sats))
    assert len(combs) == 210

    # Print out the header (suppressed by pytest, but we don't care)
    print("Number, sat1,sat2,sat3,sat4, GDOP, PDOP, HDOP, VDOP, TDOP")

    cnt = 0

    for c in combs:

        # Get the sats and generate 4 element array with the actual sats data
        sats = gps.objectsSubset(c, gps.sats)

        # Calculate ECEF coords for those 4 sats
        sats_ecef = gps.getObjectsECEFvectors(sats)

        # Calculate DOP parameters for all those sats. this should return an array
        # with 4 float values: GDOP, PDOP, HDOP, VDOP, TDOP
        dops = gps.method2(obs_lla, obs_ecef, sats_ecef)
        assert len(dops) == 5
        assert dops[0] not in [998, 999]
        assert dops[1] not in [998, 999]
        assert dops[2] not in [998, 999]
        assert dops[3] not in [998, 999]
        assert dops[4] not in [998, 999]

        # Print out the values
        print("%d, %d,%d,%d,%d,  %f, %f, %f, %f, %f" % (cnt, c[0], c[1], c[2], c[3], dops[0], dops[1], dops[2], dops[3], dops[4]))
        cnt += 1

    # Make sure the code checked 210 combinations
    assert cnt == 210

