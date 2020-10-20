from astropy import units as u
from perylune import orbit_tools
from math import pi

import pytest

# pairs of input, expected values
norm_test_cases = [ [1,1], [-pi, pi], [-4, 2*pi-4], [0, 0], [2*pi, 0], [7, 7-2*pi], [0*u.deg, 0*u.deg], [370*u.deg, 10*u.deg], \
                    [-10*u.deg, 350*u.deg]]


def test_norm_2pi():

    for inp, exp in norm_test_cases:
        assert exp == orbit_tools.normalize_2pi(inp)

def test_norm_pipi():

    for inp, exp in norm_test_cases:
        # Wrap it around by 180 degrees/pi rad
        if type(exp) == u.quantity.Quantity:
            if exp.unit == u.deg and exp.value > 180:
                exp -= 360 * u.deg
            if exp.unit == u.rad and exp.value > 2*pi:
                exp -= 2*pi*u.rad
        else:
            if exp >= pi:
                exp = exp - 2*pi

        assert exp == orbit_tools.normalize_pipi(inp)
