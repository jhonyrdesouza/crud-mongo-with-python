import pandas as pd

from pymongo import ASCENDING
from services.mongoQueries import MongoQueries
from tabulate import tabulate


class Relatorio:
    def get_relatorio_clientes(self):
        mongo = MongoQueries()
        mongo.connect()
        query = mongo.db["clientes"].find({},
                                          {"cpf": 1,
                                           "nome": 1,
                                           "telefone": 1,
                                           "email": 1,
                                           "_id": 0
                                           }).sort("nome", ASCENDING)
        clientes = pd.DataFrame(list(query))
        mongo.close()
        print('Clientes já cadastrados:')
        print(tabulate(clientes, headers='keys', tablefmt='psql'))

    def get_relatorio_fatura(self):
        mongo = MongoQueries()
        mongo.connect()

        query = mongo.db['fatura'].find({},
                                        {"id": 1,
                                         "cliente": 1,
                                         "referencia": 1,
                                         "vencimento": 1,
                                         "valor": 1,
                                         "_id": 0
                                         })
        faturas = pd.DataFrame(list(query))
        mongo.close()
        print('Faturas já emitidas:')
        print(tabulate(faturas, headers='keys', tablefmt='psql'))

    def get_relatorio_total_clientes(self):
        mongo = MongoQueries()
        mongo.connect()

        pipeline = [
            {
                '$group': {
                    '_id': '$cpf',
                    'qtd_reservas': {
                        '$sum': 1
                    }
                }
            },
            {
                '$project': {
                    'cpf': '$_id',
                    'qtd_reservas': 1,
                    '_id': 0
                }
            },
            {
                '$lookup': {
                    'from': 'fatura',
                    'localField': 'cpf',
                    'foreignField': 'cpf',
                    'as': 'fatura'
                }
            },
            {
                '$unwind': {
                    'path': '$fatura'
                }
            },
            {
                '$project': {
                    'cpf': 1,
                    'qtd_pedidos': 1,
                    '_id': 0
                }
            }
        ]
        query = mongo.db['clientes'].aggregate(pipeline)
        relatorio = pd.DataFrame(list(query))
        print(relatorio)
        input("Pressione enter para sair do relatório...")
