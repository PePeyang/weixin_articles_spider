import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def listen_task_entry():
    suber = r.pubsub()
    suber.subscribe('__keyevent@0__:expired')
    for item in suber.listen():
        print(item)

