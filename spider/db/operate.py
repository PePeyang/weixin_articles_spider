from instance import db_instance
import json
class Operate():
    def __init__(self, name):
        # self.connect()
        self.name = name
        pass

    def insert_l_in_mongo(self, document):
        return db_instance.tasks.insert_one(document)


    def get_l_in_mongo(self, biz):
        # filter(optional): a dictionary specifying the query to be performed OR
        # any other type to be used as the value for a query for "_id".
        return db_instance.tasks.find_one({'biz': biz})


    def remove_l_in_mongo(self, biz):
        return db_instance.tasks.find_one_and_delete({'biz': biz})

    # json
    def update_l_in_mongo(self, biz, update_dict):
        return db_instance.tasks.find_one_and_update(
            filter={'biz': biz},
            update={
                '$inc': {'update_count': 1},
                '$set':{
                    'User-Agent': update_dict['User-Agent'],
                    'update_time': update_dict['update_time']
                }
            }
        )


