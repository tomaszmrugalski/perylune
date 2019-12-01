# OrbCalc_test.py

from perylune.AlmanacYuma import *

import pytest

def test_loadYuma():

    alm = AlmanacYuma()
    alm.load("data/yuma/almanac.yuma-2019-11-29.txt")

    assert 31 == len(alm.sats)

    # Let's check the first sat.
    s = alm.sats[0]
    assert s.id == '01'
    assert s.name == 'PRN-01'
    assert s.e == 0.9171485901E-002
    assert s.toa == 147456.0000
    assert s.incl == 0.9783226128
    assert s.ra_rate == -0.7897471819E-008
    assert s.a == pow(5153.595215, 2)
    assert s.ra_week == -0.7699452544E-001
    assert s.aop == 0.763107131
    assert s.mean_anomaly == 0.5562066032E-001
    assert s.week == 34

    # AF0 and AF1 are ingnored upon load
