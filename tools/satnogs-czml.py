# This scripts loads the orbits database from Celestrak, finds specified
# sats, get their TLEs, convert them to poliastro's orbit and then use
# poliastro's CZML exporter to export the data to a single CZML file.
# That can be used in Cesium viewer.

from tletools import TLE
from perylune import orbitdb
from perylune import utils
from poliastro.czml.extract_czml import CZMLExtractor

db = orbitdb.OrbitDatabase()
db.refresh_urls()

def czml_generate(extr, name):
    t = db.get_name(name)

    tle = TLE.from_lines(t.name, t.line1, t.line2)

    # Convert to poliastro orbit
    orb = tle.to_orbit()

    start_epoch = orb.epoch
    end_epoch = orb.epoch + orb.period

    sample_points = 100

    extractor = CZMLExtractor(start_epoch, end_epoch, sample_points)

    extractor.add_orbit(
        orb,
        rtol=1e-4,
        label_text=name,
        groundtrack_show=True,
        label_fill_color=[125, 80, 120, 255],
    )

    return extractor.packets



def czml_write(name):
    fname = utils.safe_filename(name) + ".czml"
    pkts = czml_generate(name)
    f = open(fname, "w")
    f.write(repr(pkts))
    f.close()
    print("Content written to %s" % fname)

czml_write("NOAA 15")
czml_write("NOAA 18")
czml_write("NOAA 19")
