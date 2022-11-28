from datetime import *


class Fatura:
    def __init__(self,
                 id: int = None,
                 cliente: int = None,
                 referencia: str = None,
                 vencimento: date = None,
                 valor: int = None
                 ):

        self.set_id(id)
        self.set_cliente(cliente)
        self.set_referencia(referencia)
        self.set_vencimento(vencimento)
        self.set_valor(valor)

    def set_id(self, id: int):
        self.id = id

    def set_cliente(self, cliente: int):
        self.cliente = cliente

    def set_referencia(self, referencia: str):
        self.referencia = referencia

    def set_vencimento(self, vencimento: int):
        self.vencimento = vencimento

    def set_valor(self, valor: int):
        self.valor = valor

    def get_id(self) -> int:
        return self.id

    def get_cliente(self) -> str:
        return self.cliente

    def get_referencia(self) -> int:
        return self.referencia

    def get_vencimento(self) -> int:
        return self.vencimento

    def get_valor(self) -> int:
        return self.valor

    def to_string(self) -> str:
        return (f"ID: {self.get_id()} | Cliente: {self.get_cliente()}\n" +
                f"Referência: {self.get_referencia()} | Vencimento: {self.get_vencimento()}\n" +
                f"Valor: {self.get_valor()}")
