import redis
from pymongo import MongoClient
from configs.auth import REDIS_HOST, REDIS_PORT, REDIS_DB
from configs.auth import MONGODB_HOST, MONGODB_PORT, MONGODB_NAME

# redis
redis_instance = redis.StrictRedis(host=REDIS_HOST,
                                   port=REDIS_PORT,
                                   db=REDIS_DB,
                                   decode_responses=True)

# mongodb
mongo_client = MongoClient(MONGODB_HOST, MONGODB_PORT)
mongo_instance = mongo_client[MONGODB_NAME]
