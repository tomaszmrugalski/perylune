# Perylune

[![Build Status](https://travis-ci.com/tomaszmrugalski/perylune.svg?branch=master)](https://travis-ci.com/tomaszmrugalski/perylune)

Perylune - a [periapsis](https://en.wikipedia.org/wiki/Apsis) (a lowest point in orbit) around Luna (better known as the Moon). Also a library of tools intended to aid various calculations related to Keplerian orbits and orbital mechanics in general. The software uses great [poliastro](https://github.com/poliastro/poliastro) for most of its calculations. Currently available functionality:

- load, process and use Yuma, MPCORB (Minor Planets Center) almanacs.
- import ephemerides from NASA HORIZONS database
- import TLE data from CELESTRAK database
- calculate orbital burns, including Hohmann, prograde burns, pure inclination change
- DOP parameters calculation for GPS precision
- transfer windows (generate charts of body distances, such as Earth-Mars, Earth-Venus and others, porkchop plots)
- detailed Orbit prints (with more details than the standard Poliastro code)
- some basic time calculations

The long term goal is to be useful for the following areas:

- load, process and use various formats: SEM, 3LE
- convert coordinates between ECEF, LLA, ENU and other systems
- calculate satelite/object visibility (including rising and setting times)
- calculate ground track (single pass, design coverage for certain area, revisit times, etc.)

## Installation

```
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Alternatively, there's a make script for that:
```
make setup
```

## Additional docs

See [jupyter howto](doc/jupyter.md) for details on how to view Jupyter notebooks.

See [cesium howto](doc/cesium.md) for details on how to run Cesium (a web interface useful for visualising orbits)

See [snippets](doc/snippets.md) for a random chunks of python code that does various things.

## Developer's guide

See [tests](doc/tests.md) for details on running tests.

See [developer's guide](doc/devel.md) for developer oriented notes.
