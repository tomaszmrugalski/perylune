
from poliastro.twobody import Orbit
from poliastro.frames import Planes
from poliastro.bodies import Sun

from astropy.time import Time
from astropy import units as u

from perylune import orbit_tools

# Minor Planet Center


def download():
    # docs: https://minorplanetcenter.net/iau/info/MPOrbitFormat.html
    #
    # TODO: Download https://www.minorplanetcenter.net/iau/MPCORB/NEA.txt
    raise "Not implemented"

def parse_epoch(e):
    century = (ord(e[0])- ord('I') + 18) * 100 # I = 18, J = 19, K = 20, etc.
    year = (ord(e[1]) - ord('0')) * 10 + (ord(e[2]) - ord('0'))

    if e[3] <= '9':
        month = ord(e[3]) - ord('0')
    else:
        month = ord(e[3]) - ord('A') + 10

    if e[4] <= '9':
        day = ord(e[4]) - ord('0')
    else:
        day = ord(e[4]) - ord('A') + 10

    return Time("%d-%d-%d" % (century + year, month, day))

def parse_line(l):
    # Do the parsing in two steps. First, split the input line into shorter strings, each containing values as strings.
    epoch = l[20:25].strip()         # 21-25 epoch in packed form
    mean_anomaly = l[26:35].strip()  # in degrees
    argp = l[37:46].strip()          # argument of peryhelium J2000 (degrees)
    raan = l[48:57].strip()          # longitude of asc node J2000 (degrees)
    inc = l[59:68].strip()           # inclination
    ecc = l[70:79].strip()
    mean_motion = l[80:91].strip()   # mean daily motion (degrees/day)
    a = l[92:103].strip()            # semimajor axis (AU)

    flags = l[161:165].strip()

    name = l[166:194].strip()

    # Step 2 is to convert them to appropriate data types
    epoch = parse_epoch(epoch)
    mean_anomaly = float(mean_anomaly) * u.deg
    argp = float(argp) * u.deg
    raan = float(raan) * u.deg
    inc = float(inc) * u.deg
    ecc = float(ecc) * u.one
    mean_motion = float(mean_motion)
    a = float(a) * u.au

    print("Parsed: name[%s] epoch=[%s] mean_anomaly=[%s] argp=[%s] raan=[%s] inc=[%s] ecc=[%s] mean_motion=[%s] a=[%s] flags=[%s] epoch=%s" %
    (name, epoch, mean_anomaly, argp, raan, inc, ecc, mean_motion, a, flags, epoch))

    o = Orbit.from_classical(Sun, a, ecc, inc, raan, argp, mean_anomaly, epoch, plane=Planes.EARTH_ECLIPTIC)
    orbit_tools.print_orb(o)

    return 0

def parse_nea(limit):
    if limit is None:
        limit = 0


    f = open("NEA.txt", 'r')
    lines = f.readlines()
    f.close()

    print("Read %d line(s) from NEA.txt, parsing up to %d line(s)" % (len(lines), limit))

    orbs = []

    for l in lines:
        print("parsing: %s" % l)
        orbs.append(parse_line(l))

        if limit > 0:
            limit -= 1
            if limit == 0:
                print("Limit reached. Parsing finished.")
                return orbs

    return orbs

if __name__ == "__main__":
    x = parse_nea(limit=0)

    print("Returns %d orbit(s)" % len(x))
    print(x[0])
