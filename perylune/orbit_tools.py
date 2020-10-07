from poliastro.twobody import Orbit
from math import sqrt

def print_orb(o: Orbit):
    print(o)
    #print("Semimajor axis (), eccentricity (e), inclination (i), RAAN (Ω) - right ascension of the ascending node, argument or perigeum (𝜔), nu (𝜈) - true anomaly")
    a, e, i, raan, argp, nu = o.classical()
    b = a*sqrt(1-e*e)
    print("𝑎=%4.2f%s, b=%4.2f%s, e=%4.2f%s, i=%4.2f%s raan(Ω)=%4.2f%s argp(𝜔)=%4.2f%s nu(𝜈)=%4.2f%s" % \
        (a.value, a.unit, b.value, b.unit, e.value, e.unit, i.value, i.unit, raan.value, raan.unit, argp.value, argp.unit, nu.value, nu.unit))

def compare_orb(o1: Orbit, o2: Orbit):
    print("They do look like orbits")
