import pandas as pd

from model.clientes import Cliente
from reports.relatorios import Relatorio
from services.mongoQueries import MongoQueries
from tabulate import tabulate


class Controller_Cliente:
    def __init__(self):
        pass

    def inserir_cliente(self) -> Cliente:
        mongo = MongoQueries()
        mongo.connect()
        relatorio = Relatorio()

        relatorio.get_relatorio_clientes()
        cpf = input("\nInsira o cpf do cliente: ")
        if self.verifica_existencia_cliente(mongo, cpf):
            nome = input("\nNome completo do cliente: ")
            telefone = input('\nInsira o telefone do cliente: ')
            email = input('\nInsira o e-mail do cliente: ')

            mongo.db["clientes"].insert_one(
                {"cpf": cpf, "nome": nome, "telefone": telefone, "email": email})

            query_result = mongo.db['clientes'].find({"cpf": cpf})
            cliente = pd.DataFrame(list(query_result))

            print(f"{cliente.nome.values[0]} cadastrado com sucesso!")
            print(tabulate(cliente, headers='keys', tablefmt='psql'))

        else:
            print(f"Ops.. O CPF {cpf} já está cadastrado!")

    def atualizar_cliente(self) -> Cliente:
        mongo = MongoQueries()
        mongo.connect()

        cpf = input("CPF do cliente que deseja alterar o nome: ")

        if not self.verifica_existencia_cliente(mongo, cpf):
            novo_nome = input("Nome: ")
            mongo.db["clientes"].update_one(
                {"cpf": f"{cpf}"}, {"$set": {"nome": novo_nome}})

            query = mongo.db["clientes"].find({"cpf": cpf})
            cliente = pd.DataFrame(list(query))

            print(f"Atualizado para {cliente.nome.values[0]}!")
            print(tabulate(cliente, headers='keys', tablefmt='psql'))

        else:
            mongo.close()
            print(f"O cliente {cpf} não existe.")

    def excluir_cliente(self):
        mongo = MongoQueries()
        mongo.connect()

        cpf = input("CPF do Cliente que irá excluir: ")
        if not self.verifica_existencia_cliente(mongo, cpf):
            if not self.verifica_se_existe_fatura(mongo, cpf):

                submit = str(input(
                    "Tem certeza que quer excluir esse cliente?\n(Digite S para sim e N para não) "))
                if submit.lower() == "s":

                    query = mongo.db["clientes"].find({"cpf": cpf})

                    cliente = pd.DataFrame(list(query))
                    mongo.db["clientes"].delete_one({"cpf": f"{cpf}"})

                    print(
                        f"Cliente {cliente.nome.values[0]} excluido com sucesso!")
                    print(tabulate(cliente, headers='keys', tablefmt='psql'))

            else:
                submit = str(input(
                    "O cliente tem registro de faturas recorrentes!\nDigite s para excluir os registros e n para voltar ao menu principal."))
                if submit.lower() == "s":

                    query = mongo.db["clientes"].find({"cpf": cpf})
                    cliente = pd.DataFrame(list(query))

                    mongo.db["fatura"].delete_many({"cliente": cpf})
                    mongo.db["clientes"].delete_one({"cpf": cpf})

                    print("Cliente e faturas vinculadas removidos com sucesso!")
                    print(tabulate(cliente, headers='keys', tablefmt='psql'))
        else:
            mongo.close()
            print(f"O CPF {cpf} não existe!")

    def verifica_existencia_cliente(self, mongo: MongoQueries, cpf: int = None) -> bool:
        query = mongo.db['clientes'].find({"cpf": cpf})

        cliente = pd.DataFrame(list(query))
        return cliente.empty

    def verifica_se_existe_fatura(self, mongo: MongoQueries, cpf: int = None) -> bool:
        query = mongo.db["fatura"].find({"cpf": cpf})

        fatura = pd.DataFrame(list(query))
        return fatura.empty
