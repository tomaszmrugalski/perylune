# OrbCalc_test.py

from OrbCalc import *
import pytest

def test_deg2rad_case():
    rad = OrbCalc.deg2rad(360)
    assert rad == math.pi*2


def test_constant_rho():
    assert OrbCalc.getRho() == 180.0/math.pi

def test_constant_earth_radius():
    assert OrbCalc.getEarthRadius() == 6378137
