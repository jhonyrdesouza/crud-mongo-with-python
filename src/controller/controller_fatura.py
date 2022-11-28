import pandas as pd

from model.faturas import Fatura
from services.mongoQueries import MongoQueries
from reports.relatorios import Relatorio
from tabulate import tabulate


class Controller_Fatura:
    def __init__(self):
        pass

    def inserir_fatura(self) -> Fatura:
        mongo = MongoQueries()
        mongo.connect()
        relatorio = Relatorio()

        relatorio.get_relatorio_fatura()

        cpf = str(input("CPF do cliente para cadastro da fatura: "))
        if self.verifica_existencia_cliente(mongo, cpf):

            id = int(input("Insira o número da fatura: "))
            referencia = input('Referência: ')
            vencimento = input('Vencimento da fatura: ')
            valor = input('valor: ')

            mongo.db["fatura"].insert_one({
                "id": id,
                "cliente": cpf,
                "referencia": referencia,
                "vencimento": vencimento,
                "valor": valor
            })

            query = mongo.db['fatura'].find({"cliente": cpf})
            fatura = pd.DataFrame(list(query))

            print(
                f" Fatura de ID #{fatura.id.values[0]} cadastrado com sucesso!")
            print(tabulate(fatura, headers='keys', tablefmt='psql'))

        else:
            print(
                f'O cliente {cpf} já possui uma recorência ativa de fatura! ')

    def atualizar_fatura(self) -> Fatura:
        mongo = MongoQueries()
        mongo.connect()

        id = int(input("ID da fatura que irá alterar: "))
        if not self.verifica_existencia_fatura(mongo, id):

            novo_cpf = int(input("Insira o novo CPF do cliente: "))
            mongo.db["fatura"].update_one(
                {"id": f"{id}"}, {"$set": {"cliente": novo_cpf}})

            query = mongo.db['fatura'].find({'id': id})
            fatura = pd.DataFrame(list(query))

            print(
                f" Fatura de ID #{fatura.id.values[0]} atualizada com sucesso!")
            print(tabulate(fatura, headers='keys', tablefmt='psql'))
            mongo.close()

        else:
            mongo.close()
            print(f"O ID da fatura {id} já existe!")

    def excluir_fatura(self):
        mongo = MongoQueries()
        mongo.connect()

        id = int(input('Escolha a fatura a ser excluida: '))
        if self.verifica_existencia_fatura(mongo, id):
            print(f'A fatura {id} não existe')

        submit = str(input(
            f"Tem certeza que quer excluir a fatura #{id}? (Digite s para sim e n para não) "))
        if submit.lower() == "s":

            query = mongo.db['fatura'].find({'id': id})
            fatura = pd.DataFrame(list(query))

            mongo.db['fatura'].delete_one({'id': id})

            print(
                f" Fatura de ID #{fatura.id.values[0]} exccluída com sucesso!")
            print(tabulate(fatura, headers='keys', tablefmt='psql'))

    def verifica_existencia_cliente(self, mongo: MongoQueries, cpf: int = None) -> bool:
        query = mongo.db['clientes'].find({"cpf": cpf})

        cliente = pd.DataFrame(list(query))
        return cliente.empty

    def verifica_existencia_fatura(self, mongo: MongoQueries, id: int = None) -> bool:
        query = mongo.db['fatura'].find({'id': id})

        fatura = pd.DataFrame(list(query))
        return fatura.empty
