from perylune.czml_gen import *
from poliastro.czml.extract_czml import CZMLExtractor
from poliastro.bodies import Mars
from poliastro.examples import iss, molniya  # noqa: E402
from astropy import time
from datetime import datetime
import pytest

#@pytest.mark.skipif(True, reason="test in progress")
def test_czml_basic():

    start_epoch = time.core.Time("2020-03-27 00:00:00", scale='utc')
    end_epoch = start_epoch + 1
    sample_points = 10

    gen = CzmlGenerator(start_epoch, end_epoch, sample_points)

    assert gen is not None

    gen.extractor.add_orbit(
        molniya,
        rtol=1e-4,
        label_text="Molniya",
        groundtrack_show=True,
        label_fill_color=[125, 80, 120, 255],
    )

    f = open("tests/czml/test-czml-basic.czml", "r")

    # Make sure the content is as expected.
    assert repr(gen.extractor.packets) == f.read()

def test_czml_time():
    """Check if get_today() returns midnight of today in UTC format"""
    exp = datetime.now()
    exp_str = "<Time object: scale='utc' format='iso' value=%d-%02d-%02d 00:00:00.000>" % (exp.year, exp.month, exp.day)

    start_time = get_today()

    assert repr(start_time) == exp_str

@pytest.mark.skipif(True, reason="test in progress")
def test_czml_demo_noaa():
    from perylune import orbitdb
    odb = orbitdb.OrbitDatabase()
    odb.parse_all()
    noaa15 = odb.get_name("NOAA 15")
    noaa18 = odb.get_name("NOAA 18")
    noaa19 = odb.get_name("NOAA 19")

    assert noaa15
    assert noaa18
    assert noaa19

    f = open("tle.txt", "w")
    f.write("%s\n" % noaa15.name)
    f.write("%s\n" % noaa15.line1)
    f.write("%s\n" % noaa15.line2)
    f.write("%s\n" % noaa18.name)
    f.write("%s\n" % noaa18.line1)
    f.write("%s\n" % noaa18.line2)
    f.write("%s\n" % noaa19.name)
    f.write("%s\n" % noaa19.line1)
    f.write("%s\n" % noaa19.line2)
    f.close()

    y = 2020
    m = 2
    d = 19

    prop15 = propagate(noaa15, y, m, d, 300, 288)
    prop18 = propagate(noaa18, y, m, d, 300, 288)
    prop19 = propagate(noaa19, y, m, d, 300, 288)
    return [ prop15, prop18, prop19 ]

