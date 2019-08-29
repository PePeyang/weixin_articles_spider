from instance import db_instance
import json
import datetime

class TaskOperate():
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

    def update_crawldata_in_mongo(self, biz, update_dict):
        return db_instance.tasks.find_one_and_update(
            filter={'biz': biz},
            update={
                '$inc': {'update_count': 1},
                '$set': {
                    'start_article': update_dict['start_article'],
                    'end_article': update_dict['end_article'],
                    'total_processed': update_dict['total_processed'],
                    'update_time': datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
                }
            }
        )


class LoadsOperate():
    def __init__(self, name):
        # self.connect()
        self.name = name
        pass

    def save_list_to_db(self, list_db):
        # TODO fix
        return db_instance.loads.insert_many(list_db)
