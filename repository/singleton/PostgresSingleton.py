import psycopg2
from psycopg2 import pool

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class PostgreSQLConnectionSingleton(metaclass=SingletonMeta):
    """
    Classe para gerenciar a conexão com PostgreSQL usando o padrão Singleton.
    """
    def __init__(self, database, user, password, host, port):
        self.connection_pool = None
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=user,
                                                                      password=password,
                                                                      host=host,
                                                                      port=port,
                                                                      database=database)
            if self.connection_pool:
                print("Connection pool created successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)

    def get_connection(self):
        return self.connection_pool.getconn()

    def return_connection(self, connection):
        self.connection_pool.putconn(connection)

    def close_all_connections(self):
        self.connection_pool.closeall()
