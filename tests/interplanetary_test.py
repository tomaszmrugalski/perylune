from astropy import units as u
from perylune import interplanetary
from perylune.orbit_tools import *

from poliastro.twobody import Orbit
from poliastro.bodies import Earth, Sun
import numpy as np


def test_escape_velocity():

    # TEST CASE 1:
    # This is circular orbit, the escape velocity must be the same everywhere.
    # Escape velocity for position on the ground is 11.179km/s (source BMW2, page 30)
    o1 = Orbit.circular(Earth, 0*u.km)
    v,vp,va = interplanetary.escape_vel(o1, False)

    assert v == vp == va
    assert np.abs(v - 11179 * u.m/u.s) < 1 * u.m / u.s
    assert np.abs(vp - 11179 * u.m/u.s) < 1 * u.m / u.s
    assert np.abs(va - 11179 * u.m/u.s) < 1 * u.m / u.s

    # TEST CASE 2:
    # Escape velocity for position at the altitude of 7000km is 7719km/s (source BMW2, page 30)
    o2 = Orbit.circular(Earth, 7000*u.km)
    v,vp,va = interplanetary.escape_vel(o2, False)
    assert v == vp == va
    assert np.abs(v  - 7719 * u.m/u.s) < 1 * u.m / u.s
    assert np.abs(vp - 7719 * u.m/u.s) < 1 * u.m / u.s
    assert np.abs(va - 7719 * u.m/u.s) < 1 * u.m / u.s

    o3 = Orbit.from_classical(Earth, Earth.R + 16000 * u.km, 0.5*u.one, 0*u.deg, 0*u.deg, 0*u.deg, 0*u.deg)
    print_orb(o3)
    v,vp,va = interplanetary.escape_vel(o3, False)
    print(v, vp, va)

def close_enough(a, b, epsilon):
    assert np.abs(a - b) <= epsilon

def test_transfer_vel():
    """Tests if interplanetary Hohmann transfers are calculated properly."""

    expected = [
        # Reference: BMW 2nd ed, table 8-4, example on page 305
        ["earth", "mars", 29.79, 24.13, 32.73, 21.48, 258.84 ]
    ]

    for case in expected:
        v = interplanetary.transfer_vel(case[0], case[1], None)

        print(len(v))
        print(len(case))

        close_enough(v[0].to(u.km/u.s).value, case[2], 0.01)
        close_enough(v[1].to(u.km/u.s).value, case[3], 0.01)
        close_enough(v[2].to(u.km/u.s).value, case[4], 0.01)
        close_enough(v[3].to(u.km/u.s).value, case[5], 0.01)
        close_enough(v[4].value, case[6], 0.01)
