import pymongo


class MongoQueries:
    def __init__(self):
        self.user = "jhonyrdesouza"
        self.password = "xAI3Dej4bEjobwh2"

    def connect(self):
        self.mongo_client = pymongo.MongoClient(
            f"mongodb+srv://{self.user}:{self.password}@linky.qla5d.mongodb.net/test")
        self.db = self.mongo_client["labdatabase"]

    def close(self):
        self.mongo_client.close()
