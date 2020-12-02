#!/usr/bin/env python3

# This defines a path where the perylune sources are located.
PERYLUNE_PYTHONPATH = "/home/perylune/perylune"

# This defines a path to where the logs should be stored. In general, this should be outside of the
# web directory, so external users can't browse the log files.
PERYLUNE_LOGPATH = "/var/log/perylune/logs"

import runpy
import logging
logging.basicConfig(filename=PERYLUNE_LOGPATH + '/wsgi.log', level=logging.INFO)

logging.info('Starting perylune.wsgi')

activate_this = PERYLUNE_PYTHONPATH + '/venv/bin/activate_this.py'

runpy.run_path(activate_this)

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])

    logging.info("environ = " + repr(environ))
    yield b'Hello, World\n'
