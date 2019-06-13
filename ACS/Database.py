import redis
import json
import config

class Database():

    def __init__(self, REDIS_HOST, REDIS_PORT):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def append_user_fingerprint(self, user_id, fingerprint):
        key = "{}/fingerprints".format(user_id)
        self.redis.rpush(key, json.dumps(fingerprint))

    def get_user_fingerprints(self, user_id):
        key = "{}/fingerprints".format(user_id)
        content = self.redis.lrange(key, 0, -1)
        return [json.loads(cur) for cur in content]

database = Database(
    REDIS_HOST=config.REDIS_HOST,
    REDIS_PORT=config.REDIS_PORT
)