from perylune.czml_gen import CzmlGenerator, get_today
from poliastro.czml.extract_czml import CZMLExtractor
from poliastro.bodies import Mars
from poliastro.examples import iss, molniya  # noqa: E402
from astropy import time
from datetime import datetime
import pytest

def test_czml_basic():
    """Check if molniya orbit could be propagated"""

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
def test_czml_add_sat():
    # Need to figure out how to mock this.
    pass

@pytest.mark.skipif(True, reason="test in progress")
def test_czml_add_sats():
    pass