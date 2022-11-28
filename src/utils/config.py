MENU_PRINCIPAL = """Menu Principal
1 - Relatórios:
2 - Inserir Registros:
3 - Atualizar Registros:
4 - Remover Registros:
5 - Sair?
"""

MENU_RELATORIOS = """Relatórios
1 - Relatório de Clientes:
2 - Relatório de Faturas:
3 - Total de faturas por cliente:
0 - Sair?
"""

MENU_ENTIDADES = """Entidades
1 - Clientes:
2 - Faturas:
"""

# Consulta de contagem de registros por tabela:
def query_count(collection_name):
    from services.mongoQueries import MongoQueries
    import pandas as pd

    mongo = MongoQueries()
    mongo.connect()

    collection = mongo.db[collection_name]
    total_documentos = collection.count_documents({})
    mongo.close()
    df = pd.DataFrame({f"total_{collection_name}": [total_documentos]})
    return df


def clear_console(wait_time: int = 5):
    import os
    from time import sleep
    sleep(wait_time)
    os.system("clear")
