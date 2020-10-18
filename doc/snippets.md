


## How to import TLE data from CELESTRAK:

```python
from perylune import orbitdb
odb = orbitdb.OrbitDatabase()
odb.refresh_urls() # loads latest data from Celestrak (or uses cached version if no older than 7 days)
print(odb)
odb.get_predictor("SURCAL 159") # search TLE info by name

odb.get_name("NOAA 18")
odb.get_norad(28654)
```

## How to use TLE to create Poliastro orbit

```python
# Needed to handle TLE into Poliastro's Orbit
from poliastro.bodies import Earth
from tletools import TLE

tle_text = """GDASAT-1
1 45726U 20037D   20278.45278018  .00000608  00000-0  65390-4 0  9991
2 45726  97.7132  96.2906 0012962 283.6573  76.3213 14.92011802 14275"""
tle_lines = tle_text.strip().splitlines()
tle1 = TLE.from_lines(*tle_lines)
orb1 = tle1.to_orbit() # This returns poliastro's orbit object

a, e, i, raan, argp, nu = o.classical() # and this is how to access classical elements
```
