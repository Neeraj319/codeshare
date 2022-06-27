import redis
import os

r = redis.Redis(password=os.environ["REDIS_PASSWORD"])
