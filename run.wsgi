import sys, logging

logging.basicConfig(stream=sys.stderr)

sys.path.append('/var/www/mikeBot')

from run import app as application
