# Orbital Geometry - illumination, eclipses

import numpy as np


def solar_angle(r, s):
    """ Returns the spacecraft-earth-sun angle.
        r - spacecraft vector
        s - sun vector

        returns:
        0  - sun in zenith, Earth center in nadir
        90 - spacecraft passing over terminator
        180 - spacecraft in the eclipse """

    if s is None:
        sv = [1, 0, 0] # solar vector

    norm_r = (r[0]**2 + r[1]**2 + r[2]**2)**.5

    costheta = (sv[0]*r[0] + sv[1]*r[1] + sv[2]*r[2])/norm_r
    return np.arccos(costheta)*180/np.pi
