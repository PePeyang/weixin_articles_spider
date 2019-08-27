from instance import redis_instance
import json

# redis队列
class RQ():
    """
    使用redis创建一个队列FIFO
    """

    def __init__(self, key_name):
        """
        :param q_name:创建一个队列 开头处插入一个__BEGIN
        所有队列名称均以re__开头
        """
        self.q_name = key_name
        self.redis = redis_instance

    def push(self, data):
        """
        :param data:
        :return:1表示插入成功 0表示对象已经存在
        """
        rq = self.get_rq_data()
        if data not in rq:
            self.redis.lpush(self.q_name, data)
            return 1
        return 0

    def get(self, key):
      return self.redis.get(key)

    def pop(self):
        """
        :return:[]表示队列已经空了
        """
        data = self.redis.rpop(self.q_name)
        try:
            rq_j_data = json.loads(data)
        except:
            if data:
                rq_j_data = data.decode('utf8')
            else:
                rq_j_data = []
        return rq_j_data

    def remove(self, data):
        """
        :param data:根据data删除指定的元素
        :return:删除后的队列
        """
        rq_list = self.get_rq_data()
        self.delete_rq()
        for item in reversed(rq_list):
            if item is not data:
                self.push(item)
        rq_list = self.get_rq_data()
        return rq_list

    def delete_rq(self):
        self.redis.delete(self.q_name)


    def get_rq_data(self):
        """
        :return:返回插入的数据
        """
        rq_b_data_list = self.redis.lrange(self.q_name, 0, -1)
        rq_j_data_list = []
        for rq_b_data in rq_b_data_list:
            try:
                rq_j_data = json.loads(rq_b_data)
            except:
                rq_j_data = rq_b_data.decode('utf8')
            rq_j_data_list.append(rq_j_data)
        return rq_j_data_list

    def get_rqs(self, key):
        rqs = self.redis.keys( key + "*")
        return rqs

    def get_rqs_suffix(self, key):
        rqs = self.redis.keys("*" + key)
        return rqs


