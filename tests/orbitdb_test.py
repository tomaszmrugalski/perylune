from perylune import orbitdb
from perylune import tle
import pytest

def test_db_stats():

    db = orbitdb.OrbitDatabase()

    # Nothing is loaded by default
    assert db.count() == 0

    # There's close to 2600 sats listed for now, but the number may fluctuate over
    # time. Let's make the test robust.
    db.refresh_urls()
    assert db.count() > 2500

def test_load_db():

    db = orbitdb.OrbitDatabase()
    db.refresh_urls()

    tle1 = db.get_name("NOAA 18")
    tle2 = db.get_norad(28654)

    assert tle1 is not None
    assert isinstance(tle1, tle.tle)
    assert tle1.name == "NOAA 18"
    assert tle1.norad == 28654

    assert tle2 is not None
    assert isinstance(tle2, tle.tle)
    assert tle2.name == "NOAA 18"
    assert tle2.norad == 28654

    with pytest.raises(KeyError):
        db.get_name("nonexistent")

    with pytest.raises(KeyError):
        db.get_norad(1234567)
