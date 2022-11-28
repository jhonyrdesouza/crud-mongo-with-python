import logging
import json
from services.mongoQueries import MongoQueries

CREATE_COLLECTIONS = ["clientes", "fatura"]
logger = logging.getLogger(name="Cadastro de faturas:")
logger.setLevel(level=logging.WARNING)
mongo = MongoQueries()


def createCollections(drop_if_exists: bool = False):
    mongo.connect()
    existing = mongo.db.list_collection_names()
    for collection in CREATE_COLLECTIONS:
        if collection in existing:
            if drop_if_exists:
                mongo.db.drop_collection(collection)
                logger.warning(f"{collection} deletado(a)!")
                mongo.db.create_collection(collection)
                logger.warning(f"{collection} criado(a)!")
        else:
            mongo.db.create_collection(collection)
            logger.warning(f"{collection} criado(a)!")
    mongo.close()


def insert_many(data: json, collection: str):
    mongo.connect()
    mongo.db[collection].insert_many(data)
    mongo.close()


if __name__ == "__main__":
    logging.warning("Iniciando...")
    createCollections(drop_if_exists=True)
    logging.warning("Concluído...")
