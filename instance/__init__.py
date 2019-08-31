import redis
from pymongo import MongoClient

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0 # 第一个db
# REDIS_DB = 0  # 第一个db

MONGODB_PORT = 27017
MONGODB_HOST = '127.0.0.1'
MONGODB_NAME = 'weixindb'

# redis
redis_instance = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# mongodb
mongo_client = MongoClient(MONGODB_HOST, MONGODB_PORT)
mongo_instance = mongo_client[MONGODB_NAME]


