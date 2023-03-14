import datetime
import logging
import os
import requests
import time
from perylune.tle import tle

from orbit_predictor.sources import NoradTLESource
from orbit_predictor.predictors.base import Predictor
from perylune.conf import Config, getConfig, APP_NAME, VERSION

from perylune.utils import url_to_filename

CELESTRAK = [
    r"https://celestrak.com/NORAD/elements/active.txt"
#    "file://historic.txt"
]

class OrbitDatabase:
    def __init__(self, urls=None, max_period=7*24*60*60):
        self.max_period = max_period
        if urls is None:
            urls = CELESTRAK
        self.urls = urls

        self.tle_names = {}
        self.tle_norad = {}

        # Store all information in the ${DATADIR}/tle directory.
        cfg = getConfig()
        self.datadir = cfg.datadir + os.path.sep + 'tle'

    def _get_tle_from_url(self, url):
        if (url[:7] == "file://"):
            fname = self.datadir + os.path.sep + url[7:]
            print("Reading file [%s]" % fname)
            with open(fname, "r") as f:
                content = f.read()
                f.close()
                print("Loaded %d bytes from file %s" % (len(content), fname))
                return content

        headers = { 'user-agent': APP_NAME + " " + VERSION, 'Accept': 'text/plain' }
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as error:
            logging.error("Exception requesting TLE: %s", error)
            raise
        return response.content.decode("UTF-8")

    def _fetch_tle_and_save(self, url, tle_path):
        print("Downloading %s => %s" % (url, tle_path))

        content = self._get_tle_from_url(url)
        with open(tle_path, "w") as f:
            f.write(content)
        return tle_path

    def _get_tle_path_from_url(self, url):
        tle_filename = url_to_filename(url)

        tle_path = os.path.join(self.datadir, tle_filename)
        return tle_path

    def _get_create_time(self, path):
        stat = os.stat(path)
        ctime = stat.st_ctime
        return ctime

    def _is_out_of_date(self, path):
        ctime = self._get_create_time(path)
        now = time.time()
        return now > ctime + self.max_period

    def _get_current_tle_file(self, url: str, force_fetch=False):
        tle_path = self._get_tle_path_from_url(url)
        tle_path_exists = os.path.exists(tle_path)
        if not force_fetch and tle_path_exists and not self._is_out_of_date(tle_path):
            print("%s is up-to-date, skipping download." % tle_path)
            return tle_path

        try:
            return self._fetch_tle_and_save(url, tle_path)
        except:
            if not force_fetch and tle_path_exists:
                return tle_path
            else:
                raise

    def _is_in_source(self, source, sat_id):
        try:
            source.get_tle(sat_id, datetime.datetime.utcnow())
            return True
        except LookupError:
            return False

    def get_predictor(self, sat_id) -> Predictor:
        for url in self.urls:
            path = self._get_current_tle_file(url)
            source = NoradTLESource.from_file(path)
            if self._is_in_source(source, sat_id):
                return source.get_predictor(sat_id)
        raise LookupError("Could not find %s in orbit data." % (sat_id,))

    def refresh_satellites(self, sat_ids):
        all_sat_ids = set(sat_ids)
        found_sat_ids = set()
        for url in self.urls:
            sats_to_search = all_sat_ids.difference(found_sat_ids)
            if len(sats_to_search) == 0:
                return

            path = self._get_current_tle_file(url, force_fetch=True)
            source = NoradTLESource.from_file(path)

            for sat_id in sats_to_search:
                if self._is_in_source(source, sat_id):
                    found_sat_ids.add(sat_id)

        if all_sat_ids != found_sat_ids:
            raise LookupError("Could not find %s in orbit data." % (", ".join(all_sat_ids.difference(found_sat_ids))))

    def refresh_urls(self, force_fetch = False):
        """Downloads all defined TLE information from Celestrak and other defined sources"""
        urls = self.urls

        for url in urls:
            self._get_current_tle_file(url, force_fetch=force_fetch)
            self.parse_tlebulk(self._get_tle_path_from_url(url))

    def parse_all(self):
        for url in self.urls:
            path = self._get_current_tle_file(url)
            self.parse_tlebulk(path)

    def parse_tlebulk(self, file: str = None):
        """Parses loaded TLE data, as downloaded from CELESTRAK. The file is essentially a
           lot of TLE lines concatenated together."""

        cnt = 0
        with open(file) as f:
            lines = f.readlines()
        for i in range(int(len(lines) / 3) ):
            name = lines[3*i].strip()
            line1 = lines[3*i+1].strip()
            line2 = lines[3*i+2].strip()
            t = tle(line1, line2, name)
            self.tle_names[name] = t
            self.tle_norad[t.norad] = t
            cnt += 1
        print("Loaded %d TLEs." % cnt)

    def get_name(self, l: str) -> tle:
        """Attempts to return a TLE by its name, e.g. get_name("NOAA 18") """
        return self.tle_names[l]

    def get_norad(self, l: int) -> tle:
        """Attempts to return a TLE by its norad number, e.g. get_name(12345) """
        return self.tle_norad[l]

    def count(self) -> int:
        """Returns number of currently loaded TLEs"""
        return len(self.tle_norad)

    def __str__(self):
        """This method is used when printing the orbitdb object"""
        data = []
        for url in self.urls:
            path = self._get_tle_path_from_url(url)
            exists = os.path.exists(path)
            print("DEBUG: path=%s, url=%s" % (path, url) )
            if exists:
                out_of_date = self._is_out_of_date(path)
                creation_time = self._get_create_time(path)
                now = time.time()
                age = now - creation_time

                dt = datetime.timedelta(seconds=age)
                data.append((url, "%s: %s ago" % ("Out-of-date" if out_of_date else "Current", str(dt))))
            else:
                data.append((url, "Not exists"))

        return "\n".join("%s - %s" % (url, desc) for url, desc in data)