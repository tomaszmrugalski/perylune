# This scripts loads the orbits database from Celestrak, finds specified
# sats, get their TLEs, convert them to poliastro's orbit and then use
# poliastro's CZML exporter to export the data to a single CZML file.
# That can be used in Cesium viewer.

from astropy import time
from perylune.czml_gen import CzmlGenerator, get_today

# We can hardcode the start and end
#start_epoch = time.Time("2020-03-27 12:00", scale="utc")
#end_epoch = time.Time("2020-03-27 12:00", scale="utc")

start_epoch = get_today()
end_epoch = start_epoch + 1 # add one day

gen = CzmlGenerator(start_epoch, end_epoch, 100)
gen.add_sats([ "NOAA 15", "NOAA 18", "NOAA 19", "METEOR-M 2", "ISS (ZARYA)" ])
gen.write("data/czml/satnogs.czml")

