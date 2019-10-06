# OrbCalc_test.py

from perylune.GpsDop import *
from perylune.OrbCalc import *

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

def test_getObserverLLA():
    gps = GpsDop()
    obs_lla = gps.getObserverLLA()
    assert isinstance(obs_lla, np.ndarray)
    assert obs_lla[0] == 0.0
    assert obs_lla[1] == 0.0
    assert obs_lla[2] == 0.0


