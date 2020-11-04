from astropy import units as u
from perylune.constants import *
from poliastro.constants import GM_earth
from poliastro.bodies import Earth, Sun
from poliastro.ephem import Ephem
from poliastro.twobody import Orbit
from poliastro.util import time_range
import plotly.graph_objs as go
import numpy as np

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
