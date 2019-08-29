from instance import db_instance

class Operate():
    def __init__(self, name):
        # self.connect()
        self.name = name
        pass

    def insert_l_in_mongo(self, document):
        db_instance.tasks.insert_one(document)
        pass

    def get_l_in_mongo(self, biz):
        db_instance.tasks.find_one({'biz': biz})
        pass

    def remove_l_in_mongo(self, biz):
        db_instance.tasks.find_one_and_delete({'biz': biz})
        pass

    def update_l_in_mongo(self, biz, update):
        db_instance.tasks.find_one_and_update(
            filter={'biz': biz},
            update={
                {'$set':{
                    'User-Agent': update['User-Agent'],
                    'update_time': update['update_time']
                }},
                {'$inc': {'update_count': 1 }},
            }
        )
        pass

