# This scripts loads the orbits database from Celestrak, finds specified
# sats, get their TLEs, convert them to poliastro's orbit and then use
# poliastro's CZML exporter to export the data to a single CZML file.
# That can be used in Cesium viewer.

from tletools import TLE
from perylune import orbitdb
from perylune import utils
from datetime import date
from poliastro.czml.extract_czml import CZMLExtractor
from astropy import time

db = orbitdb.OrbitDatabase()
db.refresh_urls()

def czml_add_sat(extr, sat_name):

    print("Propagating sat %s" % sat_name)
    t = db.get_name(sat_name)

    tle = TLE.from_lines(t.name, t.line1, t.line2)

    # Convert to poliastro orbit
    orb = tle.to_orbit()

    descr = "<b>%s</b><br/><br/><b>TLE info:</b><br/>%s<br/>%s<br/><br/><b>Orbit details</b><br/>%s" % (sat_name, t.line1, t.line2, orb)

    extr.add_orbit(
        orb,
        rtol=1e-4,
        label_text=sat_name,
        id_description=descr,
        groundtrack_show=True,
        label_fill_color=[125, 80, 120, 255],
    )

def czml_write(fname, sats_list, start_epoch, end_epoch):
    fname = utils.safe_filename(fname)

    sample_points = 100

    extractor = CZMLExtractor(start_epoch, end_epoch, sample_points)

    for s in sats_list:
        czml_add_sat(extractor, s)

    f = open(fname, "w")
    f.write(repr(extractor.packets))
    f.close()
    print("Content written to %s" % fname)


start_epoch = time.Time("2020-03-22 12:00", scale="utc")
end_epoch = time.Time("2020-03-23 12:00", scale="utc")

czml_write("satnogs.czml", [ "NOAA 15", "NOAA 18", "NOAA 19", "METEOR-M 2", "ISS (ZARYA)" ] , start_epoch, end_epoch)
