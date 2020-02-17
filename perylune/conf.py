try:
    from configparser import ConfigParser, NoSectionError, NoOptionError
except ImportError:
    from ConfigParser import ConfigParser, NoSectionError, NoOptionError

import os

APP_NAME = 'perylune'
VERSION = '0.1.0'

class Config:
    db_debug = False

    datadir = ""

def getConfig(fname = "perylune.ini"):
    config = ConfigParser()
    cfg = Config()

    try:
        rootdir = os.path.dirname(os.path.realpath(__file__))
        rootdir = rootdir[:rootdir.rfind(os.path.sep)]
        inifile = rootdir + os.path.sep + fname

        if not os.path.isfile(inifile):
            raise Exception("satnogs.ini not found. Expected location: %s" % inifile)

        config.read(inifile)
        cfg.debug = config.get('server', 'debug')
        cfg.datadir = config.get('server', 'datadir')
    except IOError as e:
        raise Exception("Unable to read %s file: %s" % (inifile, e) )
    except NoSectionError as e:
        raise Exception("Unable to find section 'server' in the %s file: %s" % (inifile, e) )
    except NoOptionError as e:
        raise Exception("Unable to find option in 'server' section in the %s file: %s" % (inifile, e) )

    return cfg


