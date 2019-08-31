# 任务的队列
class Normal_queue():
    """
    创建一个队列 FIFO 先进先出
    """

    def __init__(self, q_name):
        """
        :param q_name:创建一个队列
        """
        self.q_name = q_name
        self.queue = list()

    def isEmpty(self):
        """
        判断队列是否为空
        :return:
        """
        return len(self.queue) == 0

    def pickAll(self):
        return self.queue

    def addItem(self, obj):
        """
        将指定元素加入队列的尾部
        :param obj:
        :return: self.queue
        """
        self.queue.append(obj)
        return self.queue

    def pickItem(self):
        """
        查看队首的对象，但不移除
        :return:
        """
        if not self.isEmpty():
            return self.queue[0]
        return None

    def popItem(self):
        """
        移除队首对象，并返回该对象的值
        :return:
        """
        if not self.isEmpty():
            return self.queue.pop(0)
        return None


    def empty(self):
        """
        清空队列
        :return: 被清空的队列
        """
        self.queue = list()
        return self.queue



