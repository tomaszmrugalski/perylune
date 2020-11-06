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
    o = Orbit.circular(Earth, 0*u.km)
    v,vp,va = interplanetary.escape_delta_v(o, False)

    assert v == vp == va
    assert np.abs(v - 11179 * u.m/u.s) < 1 * u.m / u.s
    assert np.abs(vp - 11179 * u.m/u.s) < 1 * u.m / u.s
    assert np.abs(va - 11179 * u.m/u.s) < 1 * u.m / u.s

    # TEST CASE 2:
    # Escape velocity for position at the altitude of 7000km is 7719km/s (source BMW2, page 30)
    o2 = Orbit.circular(Earth, 7000*u.km)
    v,vp,va = interplanetary.escape_delta_v(o2, False)
    assert v == vp == va
    assert np.abs(v  - 7719 * u.m/u.s) < 1 * u.m / u.s
    assert np.abs(vp - 7719 * u.m/u.s) < 1 * u.m / u.s
    assert np.abs(va - 7719 * u.m/u.s) < 1 * u.m / u.s

    o3 = Orbit.from_classical(Earth, Earth.R + 16000 * u.km, 0.5*u.one, 0*u.deg, 0*u.deg, 0*u.deg, 0*u.deg)
    print_orb(o2)
    v,vp,va = interplanetary.escape_delta_v(o2, False)
    print(v, vp, va)
