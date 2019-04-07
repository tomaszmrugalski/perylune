

class Orbit:
    name = ''
    id = 0

    def __init__(self, name):
        self.name = name

    def getText(self):
        return "%s: id=%s eccentricity=%f toa=%f incl=%f rate-of-ra=%f sqrt(a)=%f ra-at-week=%f aop=%f mean-anom=%f" % \
        (self.name, self.id, self.e, self.toa, self.incl, self.ra_rate, self.a_sqrt, self.ra_week, self.aop, self.mean_anomaly)
