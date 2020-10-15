from poliastro.twobody import Orbit
from astropy import units as u
import numpy as np
from math import sqrt, sin, cos

def print_orb(o: Orbit):
    print(o)
    #print("Semimajor axis (), eccentricity (e), inclination (i), RAAN (Ω) - right ascension of the ascending node, argument or perigeum (𝜔), nu (𝜈) - true anomaly")
    a, e, i, raan, argp, nu = o.classical()
    if e<1:
        b = a*sqrt(1-e*e)
    else:
        b = 0 * u.km
    a = a.to(u.m) / 1000.0
    b = b.to(u.m) / 1000.0
    apo = o.r_a.to(u.m) / 1000.0
    per = o.r_p.to(u.m) / 1000.0
    print("𝑎=%4.2f%s, b=%4.2f%s, e=%4.2f%s, i=%4.2f%s raan(Ω)=%4.2f%s argp(𝜔)=%4.2f%s nu(𝜈)=%4.2f%s period=%s perapis=%s apoapsis=%s" % \
        (a.value, a.unit, b.value, b.unit, e.value, e.unit, i.value, i.unit, raan.value, raan.unit, argp.value, argp.unit, nu.value, nu.unit, o.period, per, apo))

def compare_orb(o1: Orbit, o2: Orbit):
    print("They do look like orbits")


def inc_change(o1: Orbit, o2: Orbit):
    """
        Return delta-v cost required for pure inclination change manouver between two orbits.
        Retuns value in m/s (the returned value is using units)
    """
    di = o2.inc - o1.inc  # delta-i (the difference in inclination)
    a = o1.a.to(u.km) # semi-major axis (in meters)
    e = o1.ecc # eccentricity dimensionless
    argp = o1.argp # argument of perigeum (radians)
    nu = o1.nu # radians
    n = o1.n / u.rad # mean motion (let)

    #print("inc_change: n=%s a=%s n*a=%s (1 + ecos(nu)=%s" % (repr(n), repr(a), repr(n*a), repr(1 + e*np.cos(nu)) ))

    delta_v = 2*np.sin(di/2.0)*sqrt(1-e*e)*np.cos(argp + nu) * n * a / (1 + e*np.cos(nu))

    return delta_v


def calc_vel(o: Orbit, delta_t: u, n: int):
    """
        Calculates velocity for orbit o in n intervals, each lasting t period.
        Returned array has v(scalar), t(time)
    """
    vel = []
    orb = o
    for _ in range(1, n):
        v = orb.v # vector
        v_scalar = np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        t = orb.epoch
        vel.append([v_scalar, t, orb.nu, orb.argp])
        orb = orb.propagate(delta_t)

    return vel

def calc_vel_inc_cost(o1: Orbit, o2: Orbit, delta_t: u, n: int):
    """
        Calculates velocity for orbit o in n intervals, each lasting t period.
        Returned array has v(scalar), t(time)
    """
    vel = []
    orb = o1
    for _ in range(1, n):
        v = orb.v # vector
        v_scalar = np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        t = orb.epoch
        inc_delta_v = inc_change(orb, o2)
        vel.append([v_scalar, t, orb.nu, orb.argp, inc_delta_v])
        orb = orb.propagate(delta_t)

    return vel
