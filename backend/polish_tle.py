# This scripts loads the orbits database from Celestrak, finds specified
# sats, get their TLEs, convert them to poliastro's orbit and then use
# poliastro's CZML exporter to export the data to a single CZML file.
# That can be used in Cesium viewer.

from tletools import TLE
from perylune import orbitdb, utils, orbit_tools
from datetime import datetime, timedelta
from poliastro.czml.extract_czml import CZMLExtractor
from astropy import time
from astropy import units as u

db = orbitdb.OrbitDatabase()
db.refresh_urls()

def czml_add_sat(extr, sat):

    name = sat['name']
    descr = get_sat_descr(sat)
    orb = sat['orbit']

    print("Propagating sat %s" % name)

    # Adding custom properties requires patched poliastro code. Otherwise add_orbit will refuse properties.
    custom_props = {
            "tle1": sat['tle'].line1,
            "tle2": sat['tle'].line2
    }

    period = sat['orbit'].period.to(u.s).value

    extr.add_orbit(orb, rtol=1e-4, label_text=name, id_name=name, id_description=descr, properties = custom_props,
                   lead_time=period/2, trail_time=period/2, groundtrack_show=False) # , label_fill_color=[125, 80, 120, 255])

def czml_write(fname, sats, start_epoch, end_epoch, sample_points):

    extractor = CZMLExtractor(start_epoch, end_epoch, sample_points)

    for s in sats:
        czml_add_sat(extractor, s)

    f = open(fname, "w")
    f.write(repr(extractor.packets))
    f.close()
    print("Content written to %s" % fname)

def get_sat_descr(sat):
    name = sat['name']
    norad_id = sat['id']
    orb = sat['orbit']
    tle = sat['tle']

    RE = orb.attractor.R

    print("")
    descr =         "NORAD ID = <b>%d</b><br/><br/>\n" % norad_id
    descr = descr + "Parametry orbity<br/>\n{r_p:.1f} x {r_a:.1f} ({per_abs:.1f} x {apo_abs:.1f}) <br/>\n".format(r_p = orb.r_p, r_a=orb.r_a, per_abs=orb.r_p - RE, apo_abs=orb.r_a - RE)
    descr = descr + "Perygeum = <b>{per:.1f}</b> (wysokość {alt:.1f})<br/>".format(per = orb.r_p, alt = orb.r_p - RE)
    descr = descr + "Apogeum = <b>{apo:.1f}</b> (wysokość {alt:.1f})<br/>".format(apo = orb.r_a, alt = orb.r_a - RE)
    descr = descr + "Półoś wielka <i>a</i> = <b>%4.2f %s</b><br/>" % (orb.a.value, orb.a.unit)
    descr = descr + "Ekscentryczność <i>e</i> = <b>%s</b><br/>" % orb.ecc
    descr = descr + "Inklinacja <i>i</i> = <b>%4.2f %s</b><br/>" % (orb.inc.value, orb.inc.unit)
    descr = descr + "Rektascensja węzła wstępującego <i>raan</i> = <b>%4.2f %s</b><br/>" % (orb.raan.value, orb.raan.unit)
    descr = descr + "Argument perygeum <i>argp</i> = <b>%4.2f %s</b><br/>" % (orb.argp.value, orb.argp.unit)
    descr = descr + "Anomalia prawdziwa <i>nu</i> = <b>%4.2f %s</b><br/>" % (orb.nu.value, orb.nu.unit)
    descr = descr + "Okres = <b>{period:.1f}</b><br/>".format(period = orb.period)
    descr = descr + "Epoka = %s<br/><br/>" % str(orb.epoch)[:16]
    #descr = descr + "<br/><b>Dane TLE:</b><br/>\n<pre>%s\n%s</pre><br/>\n" % (tle.line1.strip(), tle.line2.strip())

    return descr

def process_sats(sats, start_epoch, end_epoch, sample_points, filename):

    # First we need to get process the TLE and generate the orbital data.
    for s in sats:
        try:
            t = db.get_norad(s['id'])
            tle = TLE.from_lines(t.name, t.line1, t.line2)
            orb = tle.to_orbit()
            s['orbit'] = orb
            s['tle'] = t
        except KeyError:
            print("Can't find TLE for %s (norad id %d)" % (s['name'], s['id']))

    # Now call the czml writer
    czml_write(filename, sats, start_epoch, end_epoch, sample_points)


sats = [ { "name": "PWSat", "id": 38083 },
         { "name": "PWSat-2", "id": 43814 },
         { "name": "Brite-PL (Lem)", "id": 39431 },
         { "name": "Brite-PL 2 (Heweliusz)", "id": 40119 },
         { "name": "Światowid", "id": 44426},
         { "name": "KRAKSat", "id": 44427}
     ]

# Specifies time period to generate data for: (days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
period = timedelta(days=3, minutes=0)

today = datetime.now().strftime('%Y-%m-%d')
start_epoch = time.Time(today + " 00:00", scale="utc")
end_epoch = start_epoch + period

sample_points = 1000

filename = "data/czml/polish.czml"


process_sats(sats, start_epoch, end_epoch, sample_points, filename)
