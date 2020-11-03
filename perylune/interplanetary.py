from astropy import units as u
from perylune.constants import *
from poliastro.constants import GM_earth
import numpy as np

def calc_delta_v(body1, body2):
    return 9999 * u.km/u.s

def escape_delta_v(orb, inc_correction):
    # orb - departing orbit
    # inc_correction - boolean defining whether the inclination correction should be taken into consideration or not
    # TODO: Calculate escape velocity for a body.
    planet = orb.attractor

    GM = G * planet.mass
    GM2 = GM_earth.value
    print("GM1=%s" % GM)
    print("GM2=%s [units=%s]" % (GM2, GM_earth.unit))
    print("GM_earth=%s" % GM_earth)

    print(GM - GM_earth)

    x = np.sqrt(2*GM_earth/(planet.R + 300 * u.km)) - np.linalg.norm(orb.v)
    #return 9999 * u.km/u.s
    return x

