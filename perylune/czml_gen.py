from perylune import tle, orbitdb
from tletools import TLE
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

    def init_db(self):
        """Initializes list of TLE orbits. Needed only when using add_sat() or add_sats()"""
        if 'db' in self.__dict__:
            return

        self.db = orbitdb.OrbitDatabase()
        self.db.refresh_urls()

    def add_sat(self, sat_name):

        self.init_db()

        print("Propagating sat %s" % sat_name)
        t = self.db.get_name(sat_name)

        tle = TLE.from_lines(t.name, t.line1, t.line2)

        # Convert to poliastro orbit
        orb = tle.to_orbit()

        descr = "<b>%s</b><br/><br/><b>TLE info:</b><br/>%s<br/>%s<br/><br/><b>Orbit details</b><br/>%s" % (sat_name, t.line1, t.line2, orb)

        self.extractor.add_orbit(
            orb,
            rtol=1e-4,
            label_text=sat_name,
            id_description=descr,
            groundtrack_show=True
            #label_fill_color=[125, 80, 120, 255],
        )

    def add_sats(self, sats_list):
        for s in sats_list:
            self.add_sat(s)

    def write(self, fname: str):
        """Writes content of the CzmlGenerator to a file"""
        f = open(fname, "w")
        f.write(repr(self.extractor.packets))
        f.close()
        print("Content (%d bytes) written to %s." % (len(repr(self.extractor.packets)), fname))
