from decouple import config

REDIS_HOST = config('REDIS_HOST', default='localhost', cast=str)
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
HTTP_HOST = config('HTTP_HOST', default='localhost', cast=str)
HTTP_PORT = config('HTTP_PORT', default=8484, cast=int)
PUBLIC_IP = config('PUBLIC_IP', default='localhost', cast=str)
THREE_DS_SERVER_URL = config('THREE_DS_SERVER_URL', default='http://localhost:4242', cast=str)