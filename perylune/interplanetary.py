from astropy import units as u
from astropy import time

from perylune.constants import *
from perylune.horizons import name_to_horizons_id

from poliastro.constants import GM_earth, GM_sun
from poliastro.bodies import Earth, Sun
from poliastro.ephem import Ephem
from poliastro.twobody import Orbit
from poliastro.util import time_range
from poliastro.frames import Planes
import plotly.graph_objs as go
import numpy as np

def calc_delta_v(body1, body2):
    return 9999 * u.km/u.s

def escape_vel(orb, inc_correction):
    # orb - departing orbit
    # inc_correction - boolean defining whether the inclination correction should be taken into consideration or not
    # Returns 3 escape velocities (scalars): x_cur (for current orbital position), x_per (escape velocity at periapsis) and x_apo (escape
    # velocity at apoapsis)

    # TODO: take inclination correction into consideration

    GM = orb.attractor.k # this is GM_something

    r_cur = np.linalg.norm(orb.r).to(u.m)
    r_per = orb.r_p.to(u.m)
    r_apo = orb.r_a.to(u.m)

    x_cur = np.sqrt(2*GM/(r_cur))
    x_per = np.sqrt(2*GM/(r_per))
    x_apo = np.sqrt(2*GM/(r_apo))

    return x_cur, x_per, x_apo

def escape_delta_v(orb):
    v_cur, v_per, v_apo = escape_vel(orb, False)

    # TODO: can we really just subtract one from another? Shouldn't this be a geometric subtraction?
    dv_cur = v_cur - np.linalg.norm(orb.v)
    orb = orb.propagate_to_anomaly(0*u.deg)
    dv_per = v_per - np.linalg.norm(orb.v)
    orb = orb.propagate_to_anomaly(180*u.deg)
    dv_apo = v_apo - np.linalg.norm(orb.v)

    return dv_cur, dv_per, dv_apo

def distance_chart(body1, body2, date_start, interval, steps):
    """Generates a distance chart between body1 (e.g. Earth) and body2 (e.g. Mars)
       from date_start till interval (e.g. 10 days) and steps (36).
       Returns plotly's Figure."""

    eph1 = Ephem.from_body(body1, time_range(date_start, end=date_start + steps * interval))
    eph2 = Ephem.from_body(body2, time_range(date_start, end=date_start + steps* interval))

    # Solve for departure and target orbits
    orb1 = Orbit.from_ephem(Sun, eph1, date_start)
    orb2 = Orbit.from_ephem(Sun, eph2, date_start)

    t_tbl = []
    dist_tbl = []

    t = date_start

    for i in range(1,steps):
        day = str(orb1.epoch)[:10] # take the first "2020-01-01" from the date
        t_tbl.append(day)
        dist = np.linalg.norm(orb1.r - orb2.r)
        dist_tbl.append(dist.value)

        orb1 = orb1.propagate(interval)
        orb2 = orb2.propagate(interval)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x = t_tbl, y = dist_tbl, mode="lines+markers", name="Earth - Mars distance"))

    name = body1.name + "-" + body2.name + " distance"

    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    xaxis_title="date", yaxis_title="Distance [km]", title=name,
                    margin=dict(l=20, r=20, t=40, b=20))
    return fig


def heliocentric_velocity(orbit):
    """ Calculates heliocentric velocity for a given orbit """

    if orbit.attractor != Sun:
        gm = G * orbit.attractor.mass
    else:
        gm = GM_sun

    # We could use the current distance (orbit.r), periapsis or apoapsis (orbit.r_a or orbit.r_p),
    # but we'll simply go with a = (r_a + r_p) / 2
    a = orbit.a.to(u.m)

    v = np.sqrt(gm*(1.0/a))

    return v

def hohmann_velocity(orbit1, orbit2):
    """ Calculates Hohmann parameters from orbit1 to orbit2. Assumes the orbits are co-planar.
        Returns:
        v1 - heliocentric velocity at departure on Hohmann trajectory (after burn)
        v2 - heliocentric velocity at arrival on Hohmann trajectory (before burn)
        tof - time of flight (in days) """

    r1 = orbit1.a.to(u.m)
    r2 = orbit2.a.to(u.m)

    return hohmann_velocity_from_a(r1, r2)

def hohmann_velocity_from_a(r1, r2):
    """ r1, r2 - departing orbit radius, target orbit radius.
        Returns:
        v1 - heliocentric velocity at departure on Hohmann trajectory (after burn)
        v2 - heliocentric velocity at arrival on Hohmann trajectory (before burn)
        tof - time of flight (in days) """

    E0 = GM_sun / (r1 + r2)

    v1 = np.sqrt(2*(GM_sun/r1 - E0))
    v2 = np.sqrt(2*(GM_sun/r2 - E0))

    tof = np.pi * np.sqrt( ((r1+r2)**3) / (8*GM_sun)) . to(u.day)

    return v1, v2, tof

def transfer_vel(body1, body2, attractor):
    """Returns transfer parameters for body1 (e.g. Earth) to body2 (e.g. Mars).
       Optionally, the main attractor can be specified. If omitted, Sun is assumed.

       Returns:
       helio1 - heliocentric velocity at departure (before Hohmann) (body1)
       helio2 - heliocentric velocity at arrival (body2)
       v1 - heliocentric velocity at departure (after Hohmann burn)
       v2 - heliocentric velocity at arrival (before Hohmann burn)
       tof - time of flight (in days) """

    # How to obtain the orbit. The from_horisons method seems to be no longer supported
    # as of perylune 0.16.3.
    method = "ephem" # allowed values are ephem, horizons_orbit

    if attractor is None:
        attractor = Sun

    # Let's assume the calculations are done for 2020.
    date_start = time.Time("2020-01-01 00:00", scale="utc").tdb
    date_end =   time.Time("2021-12-31 23:59", scale="utc").tdb

    name1, id_type1 = name_to_horizons_id(body1)
    name2, id_type2 = name_to_horizons_id(body2)

    if method == "ephem":
        # Get the ephemerides first and then contruct orbit based on them. This is the recommended
        # way. See warning in Orbit.from_horizons about deprecation.
        ephem1 = Ephem.from_horizons(name=name1, epochs=time_range(date_start, end=date_end), plane=Planes.EARTH_ECLIPTIC, id_type=id_type1)
        ephem2 = Ephem.from_horizons(name=name2, epochs=time_range(date_start, end=date_end), plane=Planes.EARTH_ECLIPTIC, id_type=id_type2)

        # Solve for departure and target orbits
        orb1 = Orbit.from_ephem(Sun, ephem1, date_start + 180 * u.day)
        orb2 = Orbit.from_ephem(Sun, ephem2, date_end)
    elif method == "horizons_orbit":
        # This is the old way. Sadly, it produces way better values.
        orb1 = Orbit.from_horizons(name=name1, attractor=attractor, plane=Planes.EARTH_ECLIPTIC, id_type=id_type1)
        orb2 = Orbit.from_horizons(name=name2, attractor=attractor, plane=Planes.EARTH_ECLIPTIC, id_type=id_type2)
    else:
        raise "Invalid method set."

    # The escape_delta_v returns a tuple of escape velocity at current, periapsis, apoapsis.
    helio1 = heliocentric_velocity(orb1)
    helio2 = heliocentric_velocity(orb2)

    #vesc1 = escape_vel(orb1, False)[1]
    #vesc2 = escape_vel(orb2, False)[1]

    hoh1, hoh2, tof = hohmann_velocity(orb1, orb2)

    return helio1, helio2, hoh1, hoh2, tof

def transfer_vel_header():
    txt = "# all values in km/s, except noted otherwise\n"
    txt += "#departure, arrival, heliocentric vel @ departure, heliocentric vel @ arrival, hohmann dep burn, hohmann arrival burn, time of flight [days], time of flight [years], Hohman1 delta-v, Hohmann2 delta-v"
    return txt

def transfer_vel_format(name1, name2, x, sep):
    """Used to pretty print output of transfer_vel_format.
    name1 - string defining departing body
    name2 - string defining target body
    x - tuple of 5 values returned by transfer_delta_v
    sep - optional separator. If not specified, comma (,) will be used.

    returns a string with formatted values"""

    # Set the output data separator.
    if sep is None:
        sep = ','

    # Expand the input data and convert it all to km/s
    helio1, helio2, hoh1, hoh2, tof = x
    helio1 = helio1.to(u.km/u.s)
    helio2 = helio2.to(u.km/u.s)
    hoh1   = hoh1.to(u.km/u.s)
    hoh2   = hoh2.to(u.km/u.s)

    # transfer_delta_v really returns the
    burn1 = np.abs(helio1 - hoh1)
    burn2 = np.abs(helio2 - hoh2)

    txt = "%s, %s, %4.2f, %4.2f, %4.2f, %4.2f, %4.2f, %4.3f, %4.3f, %4.3f" % (name1, name2, helio1.value,  \
        helio2.value, hoh1.value, hoh2.value, tof.value, tof.to(u.year).value, burn1.value, burn2.value )
    txt = txt.replace(",", sep)
    return (txt)

def calc_min_delta_v(departure, target):
    """ Calculates delta-v necessary to reach a target from the departure.
    departure - semi major axis of the departure orbit (a)
    target - a tuple with (name, epoch, mean_anomaly, argp, raan, inc, ecc, mean_motion, a, flags)
    Returns: delta-v necessary to reach the target """

    name, epoch, mean_anomaly, argp, raan, inc, ecc, mean_motion, a, flags = target

    r1 = departure.to(u.m)
    r2 = a.to(u.m)

    # Let's calculate Hohmann velocities
    v1, v2, tof = hohmann_velocity_from_a(r1, r2)

    v1_dep = np.sqrt(GM_sun * 1.0/r1)
    v2_arr = np.sqrt(GM_sun * 1.0/r2)

    # Now we need to adjust for the inclination change. The angle between v1 (heliocentric velocity)
    # and the v1_dep (expected Hohmann departure velocity) is inc degrees.

    # v1 - v1
    # v2 - v1_dep

    # The delta-v for departure burn also has to account for the inclination change
    dv1 = np.sqrt(v1**2 + v1_dep**2 - 2*v1*v1_dep*np.cos(inc))

    # The plain calculation is simpler (but it requires departure and arrival to be coplanar)
    # dv1_plain = abs(v1_dep - v1)
    dv2 = abs(v2_arr - v2)

    tof = np.pi * np.sqrt( ((r1+r2)**3) / (8*GM_sun)) . to(u.day)

    return dv1, dv2, dv1 + dv2, tof
