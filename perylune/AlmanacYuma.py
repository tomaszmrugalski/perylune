import sys
from perylune.Orbit import *

class AlmanacYuma:

    sats = []

    def load(self, fname):
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
                    sat = Orbit(line)
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
                    sat.a_sqrt = float(line)
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
        print("Please specify filename of an alamanac to be loaded.")
    except IOError:
        print("Error loading file")
