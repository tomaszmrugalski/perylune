from poliastro.twobody import Orbit

def print_orb(o: Orbit):
    print(o)
    print("Semimajor axis (𝑎), eccentricity (e), inclination (i), RAAN (Ω) - right ascension of the ascending node, argument or perigeum (𝜔), nu (𝜈) - true anomaly")
    print(o.classical())

def compare_orb(o1: Orbit, o2: Orbit):
    print("They do look like orbits")
