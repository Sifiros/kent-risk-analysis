from decouple import config

ACS_HOST = config('ACS_HOST', default='0.0.0.0', cast=str)
ACS_PORT = config('ACS_PORT', default=8484, cast=int)

REDIS_HOST = config('REDIS_HOST', default='redis', cast=str)
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
