# Perylune

[![Build Status](https://travis-ci.org/tomaszmrugalski/perylune.svg?branch=master)](https://travis-ci.org/tomaszmrugalski/perylune)

Perylune - a [periapsis](https://en.wikipedia.org/wiki/Apsis) (a lowest point in orbit) around Luna (better
known as the Moon). Also a library of tools intended to aid various
calculations related to Keplerian orbits and orbital mechanics in
general. The software is in very early stages of development and can't
do much at this stage. The long term goal is to be useful for the
following areas:

- load, process and use various almanach formats: Yuma, SEM, MPCORB
- convert coordinates between ECEF, LLA, ENU and other systems
- calculate satelite/object visibility (including rising and setting
  times)
- calculate ground track (single pass, design coverage for certain
  area, revisit times, etc.)
- orbital transfers (aiding mission designs, calculating delta-v
  budget, window planning)


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

## Running unit-tests

The software comes with unit-tests. You can run them using pytest. Here's how
you can do that (make sure )

```
export PYTHONPATH=.:poliastro/src
pytest -s -v
```
in the top Perylune directory.

Make sure you have current directory (.) and poliastro added to PYTHONPATH.
