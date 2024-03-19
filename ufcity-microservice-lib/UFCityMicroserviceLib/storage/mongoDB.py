import pymongo

class MongoDB:
    def __init__(self, configs):
        self.host = str(configs['host'])
        self.port = str(configs['port'])
        self.coll = configs['collection']
        self.database = configs['database']
        self.username = configs['username']
        self.password = configs['password']
        self.connection = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/"
        self.client = pymongo.MongoClient(self.connection)
        self.db = self.client[self.database]
        self.collection = self.db[self.coll]

    def create(self, key, data):
        result = self.collection.insert_one({key: data})
        return result.inserted_id

    def read(self, query={}):
        result = self.collection.find(query)
        return list(result)

    def update(self, query, data):
        result = self.collection.update_many(query, {'$set': data})
        return result.modified_count

    def delete(self, query):
        result = self.collection.delete_many(query)
        return result.deleted_count
