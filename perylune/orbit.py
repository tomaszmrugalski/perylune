

class Orbit:
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
        return "%s: id=%s eccentricity=%f toa=%f incl=%f rate-of-ra=%8e sqrt(a)=%f ra-at-week=%f aop=%f mean-anom=%f" % \
        (self.name, self.id, self.e, self.toa, self.incl, self.ra_rate, self.a, self.ra_week, self.aop, self.mean_anomaly)
