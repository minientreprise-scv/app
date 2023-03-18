import pymongo


class Database:

    def __init__(self, config):
        self.config = config

    def get(self):
        client = pymongo.MongoClient(self.get_database_url())
        return client.Plantes

    def get_database_url(self):
        mongo_user = self.config['mongodb.net']['mongo_user']
        mongo_password = self.config['mongodb.net']['mongo_password']
        mongo_server = self.config['mongodb.net']['mongo_server']
        mongo_scheme = self.config['mongodb.net']['mongo_scheme']
        return f'{mongo_scheme}{mongo_user}:{mongo_password}@{mongo_server}'
