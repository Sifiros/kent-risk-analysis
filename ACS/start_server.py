import sys
import os
import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ACS import AccessControlServer

AccessControlServer(config.HTTP_HOST, config.HTTP_PORT)