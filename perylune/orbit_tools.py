from poliastro.twobody import Orbit
from poliastro.maneuver import Maneuver
from astropy import units as u
import numpy as np
from math import sqrt, sin, cos, pi

def print_orb(o: Orbit):
    """Prints orbit details."""
    print(repr(o))
    a, e, i, raan, argp, nu = o.classical()
    if e<1:
        b = a*sqrt(1-e*e)
    else:
        b = 0 * u.km
    a = a.to(u.km)
    b = b.to(u.km)
    apo = o.r_a.to(u.km)
    per = o.r_p.to(u.km)

    # Let's also calculate above surface
    surface = o.attractor.R
    apo_surface = apo - surface
    per_surface = per - surface
    #print("Semimajor axis (𝑎), minor semi-axis (b), eccentricity (e), inclination (i), RAAN (Ω) - right ascension of the ascending node,
    #       argument or perigeum (𝜔), nu (𝜈) - true anomaly")
    print("a(𝑎)=%4.2f%s, b=%4.2f%s, e=%4.2f%s, i=%4.2f%s raan(Ω)=%4.2f%s argp(𝜔)=%4.2f%s nu(𝜈)=%4.2f%s" % \
        (a.value, a.unit, b.value, b.unit, e.value, e.unit, i.value, i.unit, raan.value, raan.unit, argp.value, argp.unit, nu.value, nu.unit))
    print("period=%4.2f%s perapis=%4.0f%s(%4.2f%s) apoapsis=%4.0f%s(%4.2f%s)" % \
        (o.period.value, o.period.unit, \
         per.value, per.unit, per_surface.value, per_surface.unit, \
         apo.value, apo.unit, apo_surface.value, apo_surface.unit))

def compare_orb(o1: Orbit, o2: Orbit):
    """Compares two orbits"""
    # TODO: Implement this
    print("They do look like orbits")


def inc_change(o1: Orbit, o2: Orbit):
    """
        Return delta-v cost required for pure inclination change manouver between two orbits.
        Retuns value in m/s (the returned value is using units)

        Reference: https://en.wikipedia.org/wiki/Orbital_inclination_change#Calculation

        Note: The equation on wikipedia is slightly broken. The cost(arg of periapsis + true anomaly) should be inside the
        square root.
    """
    di = o2.inc - o1.inc  # delta-i (the difference in inclination, in degrees or radians)
    a = o1.a.to(u.km) # semi-major axis (in kilometers)
    e = o1.ecc # eccentricity dimensionless
    argp = o1.argp # argument of perigeum (radians)
    nu = o1.nu # true anomaly (nu), in radians
    n = o1.n / u.rad # mean motion (rad/s)

    delta_v = 2*np.sin(di/2.0)*sqrt(1-e*e*np.cos(argp + nu)) * n * a / (1 + e*np.cos(nu))

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
        Returned array has v(scalar), t(time), nu(), argument of perigeum, delta-v of incination change, r (distance from
        attractor center)
    """
    vel = []
    orb = o1
    for _ in range(1, n):
        v = orb.v # vector
        v_scalar = np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        t = orb.epoch
        inc_delta_v = inc_change(orb, o2)
        r = np.linalg.norm(orb.r) # Distance from Earth center
        vel.append([v_scalar, t, orb.nu, orb.argp, inc_delta_v, r])
        orb = orb.propagate(delta_t)

    return vel

def normalize_2pi(a):
    """Normalizes value to <0..2pi) range.
       This works for float, u.deg and u.rad types. """
    if (type(a) == u.quantity.Quantity):
        if (a.unit == u.deg):
            return np.mod(a, 360*u.deg)
        if (a.unit == u.rad):
            return np.mod(a, 2*pi*u.rad)
    else:
        # float
        return a % (2*pi)

def normalize_pipi(a):
    """Normalizes value to <-pi...pi) range"""
    if (type(a) == u.quantity.Quantity):
        if (a.unit == u.deg):
            return np.mod(a + 180*u.deg, 360*u.deg) - 180*u.deg
        if (a.unit == u.rad):
            return np.mod(a + pi*u.rad, 2*pi*u.rad) - pi*u.rad
    else:
        # float
        return (a + pi) % (2*pi) - pi

def propagate_to_periapsis(o: Orbit):
    """ Propagate given orbit to its periapsis. """
    if o.nu != 0 * u.deg:
        o_f = o.propagate_to_anomaly(0 * u.deg)
        return o_f
    return o

def calculate_nodes_dist(o: Orbit):
    """Calculates radial distance to ascending and decending nodes.
       Returns an, dn, dan, ddn
       an - ascending node (in radians from periapsis)
       dn - descending node (in radians from periapsis)
       dan - distance from current position to ascending node (in radians)
       ddn - distance from current position to descending node (in radians)"""

    nu = o.nu.to(u.deg)
    argp = o.argp.to(u.deg)
#    print("nu=%s" % nu)
#    #print("argp=%s" % argp)
    an = normalize_2pi(- argp)
    dn = normalize_2pi(an + 180*u.deg)

    dist_to_an = normalize_2pi(an - nu)
    dist_to_dn = normalize_2pi(dn - nu)

    return an, dn, dist_to_an, dist_to_dn

def propagate_to_asc_node(o: Orbit):
    """ Propagates the orbit to the ascending node."""
    an, _, _, __ = calculate_nodes_dist(o)

    o_f = o.propagate_to_anomaly(an)
    return o_f

def propagate_to_desc_node(o: Orbit):
    """ Propagates the orbit to the descending node."""
    _, dn, _, _ = calculate_nodes_dist(o)

    o_f = o.propagate_to_anomaly(dn)
    return o_f


# def sync_raan_inc(o1: Orbit, raan_f, inc_f):
#     """ Generates a maneuver that will achieve specified RAAN and inclination.
#         Based on Braeunig, http://www.braeunig.us/space/orbmech.htm#maneuver, see eq. 4.75 and the text above it. """


def prograde_maneuver(o: Orbit, dv, delay):
    """ Generates maneuver in the prograde direction.
        dv - expressed as dimensionless float (in m/s)
        delay - delay expressed as u.s (in seconds) """

    if delay is None:
        delay = 0*u.s

    # If the units used are km rather than m, then we need to shrink the dv value by 3 orders of magnitude
    if o.v[0].unit == u.km / u.s:
        dv /= 1000

    # normalize v
    len = np.linalg.norm(o.v)
    vnorm = o.v / len.value
    v = vnorm * dv

    print(v)

    man = Maneuver((delay, v))

    return man

def plane_change_maneuver(o: Orbit, theta):
    """ Generates inclination change maneuver. This changes the inclination by theta degress.
        o - initial orbit
        theta - expressed in plain float as degrees or as u.deg. This maneuver in general should be
        performed at either ascending or descending node.

        returns:
        maneuver that can be applied on the initial orbit.

        To perform this calculation, a local coords system is needed. (i,j,k) unit vectors are defined.
        The coords system is oriented as follows:

       j^ (normal vector)
        |
        |
        |
        +---------->    (velocity vector) ----------- orbital plane
       k             i

        (towards viewer = r vector, from Earth center to spacecraft)

        In this coords system, the inclination change is done in i,j plane.

                   _^
              vf__/  \
             __/      \ dv = vf - v
          __/          \
         /              \
        +---------------->
                v

        First we need to calculate the expected final velocity (vf). The get the delta-v vector as
        a difference of vf minus the original velocity.

         """

    # Let's assume the delay is not configurable and the maneuver always takes place immediately.
    delay = 0*u.s

    if type(theta) == float:
        theta = theta * u.deg

    # Get the v (current velocity) and r (distance from Earth center) as vectors and make both of them dimiensionless
    # Also convert them to km first. We want to get rid of the units, because they complicate the cross product.
    v = o.v.to(u.km / u.s) / u.km * u.s
    r = o.r.to(u.km) / u.km

    # This is a normal vector. It is perpendicular to the plane defined by r (connected Earth center with the object) and v (velocity)
    # This has the right direction.
    normal = np.cross(v,r)
    # Now we need to calculate the right vectors magnitude
    normal = normal / np.linalg.norm(normal).value

    # Let's get 3 unit vectors and the r,v,n mangitudes (lenghts) expressed as floats
    v_len = np.linalg.norm(v).value
    n_len = np.linalg.norm(normal).value
    r_len = np.linalg.norm(r).value

    # get the unit vectors
    i = v / v_len
    j = normal / n_len
    k = r / r_len

    #print("i=%s" % i)
    #print("j=%s" % j)
    #print("k=%s" % k)

    # final velocity after maneuver
    vf = i * v_len * np.cos(theta) + j * v_len * np.sin(theta)

    #print("vf=%s" % vf)

    # The maneuver dv is a difference between original and final velocity
    dv = vf - v
    dv = dv * u.km / u.s

    # Ok, turn this into maneuver and we're done!
    man = Maneuver((delay, dv))

    return man
