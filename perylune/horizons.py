import urllib.request
import os.path
from math import sqrt

import plotly.graph_objs as go

from astropy import units as u

from astropy.time import Time, TimeDelta

from poliastro.plotting.static import StaticOrbitPlotter
from poliastro.util import time_range

from astropy.coordinates import solar_system_ephemeris
from poliastro.bodies import Earth, Mars, Sun, Moon
from poliastro.ephem import Ephem

def get_ephem(name, start_time, stop_time):


    COMMAND= name # '1998 OR2'
    CENTER= '500@399'
    MAKE_EPHEM= 'YES'
    TABLE_TYPE= 'VECTORS'
    START_TIME= start_time # '2020-04-20'
    STOP_TIME= stop_time # '2020-05-10'
    STEP_SIZE= '1%20d' # '1 d'
    OUT_UNITS= 'KM-S'
    REF_PLANE= 'ECLIPTIC'
    REF_SYSTEM= 'J2000'
    VECT_CORR= 'NONE'
    VEC_LABELS= 'YES'
    VEC_DELTA_T= 'NO'
    CSV_FORMAT= 'YES'
    OBJ_DATA= 'YES'
    VEC_TABLE= '3'

    fname = "%s-%s-%s.txt" % (name, start_time, stop_time)

    if (os.path.isfile(fname)):
        print("Local copy exists for %s (start date; %s, end date:%s ), using." % (name, start_time, stop_time))
        f = open(fname, 'r')
        txt = f.read()
        f.close()
        print("Read %d bytes from %s" % (len(txt), fname))
        return txt


    print("Downloading data from ssd.jpl.nasa.gov")
    BASE_URL="https://ssd.jpl.nasa.gov/horizons_batch.cgi"


    URL = "%s?batch=1&COMMAND='%s'&CENTER='%s'&MAKE_EPHEM='%s'&TABLE_TYPE='%s'&START_TIME='%s'&STOP_TIME='%s'&STEP_SIZE='%s'&OUT_UNITS='%s'&REF_PLANE='%s'" \
        "&REF_SYSTEM='%s'&VECT_CORR='%s'&VEC_LABELS='%s'&VEC_DELTA_T='%s'&CSV_FORMAT='%s'&OBJ_DATA='%s'&VEC_TABLE='%s'" % \
        (BASE_URL, COMMAND, CENTER, MAKE_EPHEM, TABLE_TYPE, START_TIME, STOP_TIME, STEP_SIZE, OUT_UNITS, REF_PLANE, REF_SYSTEM, VECT_CORR, \
        VEC_LABELS, VEC_DELTA_T, CSV_FORMAT, OBJ_DATA, VEC_TABLE)

    print("URL=%s" % URL)

    with urllib.request.urlopen(URL) as f:
        html = f.read().decode('utf-8')

    print("Retrieved %d bytes from SSD" % len(html))

    print("Writing to %s" % fname)
    f = open(fname, 'w')
    f.write(html)
    f.close()

    return html

def process_ephem(txt):
    """Processes text response"""

    lines = txt.splitlines()

    data = []

    # First isolate the lines with actual data. The section starts with $$SOE and ends with $$EOE
    found = False
    cnt = 0
    for l in lines:
        cnt += 1
        if not found and l != "$$SOE":
            continue
        if l == "$$SOE":
            found = True
            #print("Found data start in line %d" % cnt)
            continue

        if found and l == "$$EOE":
            found = False
            #print("Found end of data in line %d" % cnt)
            continue

        data.append(l)

    print("Found %d lines of data" % len(data))

    # JDTDB, Calendar Date (TDB), X, Y, Z, VX, VY, VZ, LT, RG, RR,
    ephem = []
    for l in data:
        cells = l.split(',')
        jd = cells[0].strip()
        date = cells[1].strip()
        x = float(cells[2].strip())
        y = float(cells[3].strip())
        z = float(cells[4].strip())
        dist = sqrt(x**2 + y**2 + z**2)
        ephem.append([jd, date, x, y, z, dist])

    return ephem

def print_data(pos):
    for l in pos:
        print("Distance at %s: %4.0f km" % (l[1], l[5]))

def extract_data(pos):

    dates = []
    dist = []

    for l in pos:
        dates.append(l[1][10:16])
        dist.append(l[5])

    return dates, dist


def dist_plot(dates, dist, title):
    """ 
    Generates distance plot. 

    dates - array of x values
    dist - array of y values
    title - string with the chart title

    returns plotly figure (call .show() on it to display)
    """

    fig = go.Figure()
    fig.add_trace(go.Scatter(x = dates, y = dist, mode="markers", name="Delta-v [km/s]"))

    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), 
                      xaxis_title="date", yaxis_title="Distance [km]", title=title,
                      margin=dict(l=20, r=20, t=40, b=20))

    return fig

def dist_chart(asteroid, date, timespan):
    solar_system_ephemeris.set('jpl')

    EPOCH = Time(date, scale="tdb")

    epochs = time_range(
        EPOCH - TimeDelta(timespan), end=EPOCH + TimeDelta(timespan)
    )

    epochs_moon = time_range(
        EPOCH - TimeDelta(15 * u.day), end=EPOCH + TimeDelta(15 * u.day)
    )

    moon = Ephem.from_body(Moon, epochs_moon, attractor=Earth)
    aster = Ephem.from_horizons(asteroid, epochs, attractor=Earth)

    plotter = StaticOrbitPlotter()
    plotter.set_attractor(Earth)
    plotter.set_body_frame(Moon)
    plotter.plot_ephem(moon, EPOCH, label=Moon);
    plotter.plot_ephem(aster, EPOCH, label=asteroid);

    return plotter

if __name__ == '__main__':
# Example usage:
    txt = get_ephem("1998%20OR2", "2020-04-20", '2020-05-10')
    pos = process_ephem(txt)
    print_data(pos)

