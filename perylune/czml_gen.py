from perylune import tle
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from typing import Sequence
from astropy import time
from datetime import datetime

from poliastro.czml.extract_czml import CZMLExtractor
from poliastro.bodies import Body

def get_today():
    """Returns midnight of today's date in UTC"""
    tmp = datetime.now()
    return time.core.Time("%s-%s-%s 00:00:00" % (tmp.year, tmp.month, tmp.day), scale='utc')

class CzmlGenerator():
    def __init__(self, start_epoch: time.core.Time, end_epoch: time.core.Time, sample_points: int,
                attractor: Body = None, pr_map: str = None, scene3D : bool = True):
        self.extractor = CZMLExtractor(start_epoch, end_epoch, sample_points, attractor, pr_map, scene3D)

    def f(self, start_epoch: time.core.Time = 0):
        pass


    def write(self, fname: str):
        """Writes content of the CzmlGenerator to a file"""
        f = open(fname, "w")
        f.write(repr(self.extractor.packets))
        f.close()

"""
        Orbital constructor

        Parameters
        ----------
        start_epoch: ~astropy.time.core.Time
            Starting epoch
        end_epoch: ~astropy.time.core.Time
            Ending epoch
        N: int
            Default number of sample points.
            Unless otherwise specified, the number
            of sampled data points will be N when calling
            add_orbit()
        attractor: poliastro.Body
            Attractor of the orbits
        pr_map: str
            A URL to the projection of the defined ellipsoid (UV map)
        scene3D: bool
            Determines the scene mode. If set to true, the scene
            is set to 3D mode, otherwise it's the orthographic
            projection.
        """
