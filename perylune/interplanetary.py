from astropy import units as u
from perylune.constants import *
from poliastro.constants import GM_earth
import numpy as np
from poliastro.bodies import Earth

def calc_delta_v(body1, body2):
    return 9999 * u.km/u.s

def escape_delta_v(orb, inc_correction):
    # orb - departing orbit
    # inc_correction - boolean defining whether the inclination correction should be taken into consideration or not
    # Returns 3 escape velocities: x_cur (for current orbital position), x_per (escape velocity at periapsis) and x_apo (escape
    # velocity at apoapsis)
    planet = orb.attractor

    GM = G * planet.mass
    if (planet.name == "Earth"):
        GM = GM_earth


    orb_per = orb.propagate_to_anomaly(0*u.deg)
    orb_apo = orb.propagate_to_anomaly(180*u.deg)

    r_cur = np.linalg.norm(orb.r).to(u.m)
    r_per = np.linalg.norm(orb_per.r).to(u.m)
    r_apo = np.linalg.norm(orb_apo.r).to(u.m)

    x_cur = np.sqrt(2*GM/(r_cur)) - np.linalg.norm(orb.v) # current orbital position
    x_per = np.sqrt(2*GM/(r_per)) - np.linalg.norm(orb_per.v) # current orbital position
    x_apo = np.sqrt(2*GM/(r_apo)) - np.linalg.norm(orb_apo.v) # current orbital position

    return x_cur, x_per, x_apo

