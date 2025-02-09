"""
Padrão utilizado: Singleton.
Explicação:
Garante que exista apenas uma instância de conexão com o banco de dados durante a execução da aplicação,
centralizando o gerenciamento do acesso aos dados e evitando conflitos ou múltiplas conexões desnecessárias.
"""


import sqlite3

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect("professores.db")
            cls._instance.cursor = cls._instance.conn.cursor()
        return cls._instance

    def executar(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def buscar(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fechar(self):
        self.conn.close()
        self.conn = None
        self.cursor = None
        Database._instance = None