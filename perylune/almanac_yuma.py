import sys

from poliastro.twobody import Orbit
from poliastro.bodies import Earth
from astropy import units as u

class OrbitYuma:
    name = ''
    id = 0

    def __init__(self, name):
        self.name = name        # Name of the object
        self.id = 0             # Id of an object

        self.e = 0.0            # Orbit eccentricity (0-inf), 0=circular, 0..1 - eliptical, 1=parabolic, >1 for hyperbolic.
        self.a = 0.0            # Major semi-axis
        self.incl = 0.0         # Orbit Inclination (degrees 0-359.9)
        self.toa = 0.0          #
        self.ra_rate = 0.0      #
        self.ra_week = 0        #
        self.aop = 0            #
        self.mean_anomaly = 0.0 #

        self.week = 0           # Yuma only

    def getText(self):
        return "%s: id=%s eccentricity=%f toa=%f incl=%f rate-of-ra=%8e a=%f ra-at-week=%f aop=%f mean-anom=%f" % \
        (self.name, self.id, self.e, self.toa, self.incl, self.ra_rate, self.a, self.ra_week, self.aop, self.mean_anomaly)

    def to_orbit(self):
        """Returns Orbit object from Poliastro."""

        # TODO: Calculate epoch
        o = Orbit.from_classical(Earth, self.a * u.m, self.e * u.one, self.incl * u.rad, self.ra_week * u.rad, self.aop * u.rad, self.mean_anomaly * u.rad)
        return o

class AlmanacYuma:

    sats = []

    def load(self, fname, append=True):
        """loads YUMA almanac from a file. append controls whether to keep existing
           sats info or not. Loaded sats are stored in self.sats """
        if not append:
            self.sats.clear()
        try:
            sat = None
            for line in open(fname,'r').readlines():
                # Check if this is a line starting new satellite
                # ******** Week 0 almanac for PRN-01 ********
                offset = line.find('almanac for ')
                if offset != -1:
                    line = line[offset+12:]
                    line = line.replace('*','')
                    line = line.strip()
                    if sat is not None:
                        self.sats.append(sat)
                    sat = OrbitYuma(line)
                    continue

                # Check if this is a line defining ID
                # ID:                         01
                offset = line.find('ID:')
                if offset != -1:
                    line = line[26:]
                    sat.id = line.strip()
                    continue

                # Check if this is a line defining eccentricity
                #Eccentricity:               0.8619308472E-002
                offset = line.find('Eccentricity:')
                if offset != -1:
                    line = line[26:]
                    sat.e = float(line)
                    continue

                # Time of Applicability(s):
                offset = line.find('Time of Applicability(s):')
                if offset != -1:
                    line = line[26:]
                    sat.toa = float(line)
                    continue

                # inclination
                offset = line.find('Orbital Inclination')
                if offset != -1:
                    line = line[26:]
                    sat.incl = float(line)
                    continue

                # rate of RA
                offset = line.find('Rate of Right Ascen')
                if offset != -1:
                    line = line[26:]
                    sat.ra_rate = float(line)
                    continue

                # sqrt(a)
                offset = line.find('SQRT(A)')
                if offset != -1:
                    line = line[26:]
                    sat.a = float(line) ** 2
                    continue

                # Right ascenstion at week
                offset = line.find('Right Ascen at Week')
                if offset != -1:
                    line = line[26:]
                    sat.ra_week = float(line)
                    continue

                # Argument of Perigee
                offset = line.find('Argument of Perigee')
                if offset != -1:
                    line = line[26:]
                    sat.aop = float(line)
                    continue

                # Mean Anomaly
                offset = line.find('Mean Anom')
                if offset != -1:
                    line = line[26:]
                    sat.mean_anomaly = float(line)
                    continue

                # Week
                offset = line.find('week:')
                if offset != -1:
                    line = line[26:]
                    sat.week = int(line)
                    continue

                #AF0, AF1 ignored for now

            self.sats.append(sat)

        except IOError:
            print("Failed to open %s file" % fname)

    def printAll(self):
        print("Loaded %d sat(s)" % len(self.sats))
        i = 0
        for s in self.sats:
            print("%d: %s" % (i, s.getText()))
            i = i + 1

if __name__ == '__main__':

    try:
        filename = sys.argv[1]
        print("Loading file %s" % filename)

        app = AlmanacYuma()
        app.load(filename)

        app.printAll()
    except IndexError:
        print("Please specify filename of a Yuma almanac to be loaded.")
    except IOError:
        print("Error loading file")
