from astropy import units as u
from perylune import geom
import numpy as np

import pytest

def close_enough(a, b, epsilon):
    assert np.abs(a - b) <= epsilon

def test_solar_angle():

    # [x,y,z, exp_angle]
    cases = [ [1, 0, 0, 0],
              [-1, 0, 0, 180],
              [0, 1, 0, 90],
              [0,-1, 0, 90],
              [0, 0, 1, 90],
              [0, 0,-1, 90],
              [1, 1, 0, 45],
              [1,-1, 0, 45],
              [1, 1, 0, 45],
              [-1, 1, 0, 135] ]

    for case in cases:
        r = case[:3]
        #print("Checking vector %s, expecting angle %f" % (r, case[3]))
        close_enough(geom.solar_angle(r, None), case[3], 0.00001)
