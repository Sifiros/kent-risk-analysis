import sys
import os
import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ACS import AccessControlServer

AccessControlServer(config.ACS_HOST, config.ACS_PORT)