# Interesting links

https://www.reddit.com/r/Kos/comments/5h509a/hoe_do_you_calculate_intersecting_points_of_two/

https://space.stackexchange.com/questions/13632/transfer-between-elliptical-orbits
Nice discussion about transfer between elliptical orbits

Angry astronaut - Earth-Moon system delta-v map
https://youtu.be/Lb3t1rvQ-60?t=712

# UI Ideas

- orbit editor (orbit + add realistic maneuvers)
  - scenario: suborbital Perun launch. Task: make it to the orbit

# Stuff to figure out

1. Convert long, lat to Cartesian

This works in Cesium:

let tkis = Cesium.Cartesian3.fromDegrees(18.531787, 54.352469);
console.log(tkis)

and returns this (which seems correct in Cesium):
Object { x: 3532232.772395696, y: 1184047.9870634037, z: 5159706.471019858 }

This doesn't work in python:

import astropy.coordinates
import astropy.constants
from math import pi
stropy.coordinates.spherical_to_cartesian(astropy.constants.R_earth, 54.352469/180.0*pi, 18.351787/180.0*pi)

(<Quantity 3528090.50317684 m>, <Quantity 1170343.09459393 m>, <Quantity 5182956.11136441 m>)

Those values are a bit off (located at Gdansk Bay rather then where it's supposed)

-----

# Poliastro + jupyter installation

python -m venv venv
source venv/bin/activate

pip install wheel
pip install poliastro

pip install jupyterlab

pip install tle-tools

jupyterlab

# POLIASTRO CONTRIB IDEAS

- doc update explaining how to tweak the charts
  (see 02-rocketlab-to-noaa17.ipynb)
  plot.plot(orb1, color="orange", label="GDASAT-1, after orbital insertion")
  plot.plot(orb_target, color="red", label="NOAA-17, target sat")
  plot._layout.width=1200
  plot._layout.height=800

  the _layout is not documented anywhere.
  there is no description whatsoever how to alter the legend.

- Implement Jacchia-77 atmospheric model (90-2500km), the standard COESA 1962 and 1976 models cover 0-700 and 0-1000km.

- Pass custom properties to CZML exporter. Example usage: pass TLE data, so it can be visualized easily.
  1. poliastro/czml/extract_czml.pl:
  Two new parameters to add_orbit:
          properties=None,
          groundtrack_properties=None,
  2. Pass properties=properties when creating packet
  3. Pass properties=groundtrack_properties when creating groundtrack packet
- Add lead_time and trail_time to czml.add_orbit (see )

# Other Notes

- POLIASTRO BUG: importing orbit from Horizons ephemerides for Earth around Sun shows odd inclination
  (note to self: setting up right plane fixes that) The default should be updated.

- atmospheric perturbers doc
  C_D = 2.2  # dimentionless => dimensionless

- https://docs.poliastro.space/en/latest/examples/Atmospheric%20models.html
  Last series of charts, the first chart has incorrect x axis description.

  axs[0].set_xlabel("T [K]")
  axs[0].set_xlabel("Altitude [K]")  <- remove this one

- missing hypothesis in requirements.{in|txt}
