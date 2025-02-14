import requests
import json

from repository.singleton.PostgresSingleton import PostgreSQLConnectionSingleton


def llama():
    url = "http://localhost:4891/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "Llama-3.2-3B-Instruct",
        "messages": [{"role": "user", "content": "Quem é Lionel Messi?"}],
        "max_tokens": 50,
        "temperature": 0.28
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Resposta:", response.json())
    else:
        print("Erro:", response.status_code, response.text)


def testbd():
    # Configurações de conexão
    database = "postgres"
    user = "postgres"
    password = "4667"
    host = "localhost"
    port = "5432"

    from repository.repository import PerfilRepository

    # Obtendo instância Singleton
    postgres_connection = PostgreSQLConnectionSingleton(database, user, password, host, port)

    # Obtendo uma conexão
    conn = postgres_connection.get_connection()

    # Utilizando a conexão (Exemplo de consulta)
    with conn.cursor() as cursor:
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    # Retornando a conexão para o pool
    postgres_connection.return_connection(conn)

    # Fechando todas as conexões
    postgres_connection.close_all_connections()


if __name__ == "__main__":
    from interface.interface import interface

    # llama()
    # testbd()
    #
    # from repository.repositories import PerfilRepository
    #
    # # Criar instância do repositório
    # perfil_repo = PerfilRepository()
    #
    # # Executar o metodo get_perfil
    # perfil_id = 1
    # perfil = perfil_repo.get_perfil(perfil_id)
    # print(perfil)
    #
    # # Certifique-se de fechar a conexão ao finalizar
    # perfil_repo.close_connection()

    interface()
