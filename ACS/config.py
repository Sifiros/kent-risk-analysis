from decouple import config

REDIS_HOST = config('REDIS_HOST', default='redis', cast=str)
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
HTTP_HOST = config('HTTP_HOST', default='localhost', cast=str)
HTTP_PORT = config('HTTP_PORT', default=8484, cast=int)

