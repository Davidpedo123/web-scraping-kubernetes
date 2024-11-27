"""import redis
import os

HOST_REDIS = os.environ['HOST_REDIS']
PORT_REDIS = os.environ['PORT_REDIS']
PASSWD_REDIS = os.environ['PASSWD_REDIS']
redis_client = redis.StrictRedis(host=HOST_REDIS, port=PORT_REDIS, password=PASSWD_REDIS, db=0)