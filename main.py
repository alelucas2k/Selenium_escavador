"""
Padrão utilizado: Facade.
Explicação:
Este é o ponto de entrada da aplicação que orquestra as operações de inicialização,
como a configuração do banco de dados e o disparo do fluxo de scraping.
Ele simplifica a interação entre os diversos componentes do sistema, oferecendo uma interface única e coesa.
"""


import os
from dotenv import load_dotenv
from scraper_facade import ScraperFacade
from database import Database

# Carregar variáveis do .env
load_dotenv()

def main():
    try:
        db = Database()

        # Criar tabela se não existir
        db.executar(
            "CREATE TABLE IF NOT EXISTS professores ("
            "id INTEGER PRIMARY KEY, "
            "nome TEXT UNIQUE, "
            "status TEXT DEFAULT 'pendente', "
            "resumo TEXT)"
        )

        # Verificar se a coluna 'status' existe
        colunas = db.buscar("PRAGMA table_info(professores)")
        status_existe = any(coluna[1] == 'status' for coluna in colunas)
        resumo_existe = any(coluna[1] == 'resumo' for coluna in colunas)

        if not resumo_existe:
            db.executar("ALTER TABLE professores ADD COLUMN resumo TEXT")
        if not status_existe:
            db.executar("ALTER TABLE professores ADD COLUMN status TEXT DEFAULT 'pendente'")

        # 🔹 Carregar professores do .env
        professores = os.getenv("PROFESSORES_LIST", "").split(",")

        # Inserir professores no banco (se não existirem)
        for professor in professores:
            professor = professor.strip()  # Remover espaços extras
            if professor:
                try:
                    db.executar("INSERT OR IGNORE INTO professores (nome) VALUES (?)", (professor,))
                except Exception as e:
                    print(f"Erro ao inserir professor {professor}: {e}")

        # Criar o scraper
        scraper = ScraperFacade()

        # Processar professores pendentes
        professores_pendentes = db.buscar("SELECT nome FROM professores WHERE status = 'pendente'")

        if not professores_pendentes:
            print("Nenhum professor pendente encontrado.")
            return

        print(f"Processando {len(professores_pendentes)} professores...")

        for professor in professores_pendentes:
            try:
                print(f"\nIniciando busca por: {professor[0]}")
                scraper.buscar_professor(professor[0])
            except Exception as e:
                print(f"Erro durante scraping de {professor[0]}: {e}")

    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        if 'scraper' in locals():
            scraper.fechar()
        if 'db' in locals():
            db.fechar()
        print("Processo finalizado.")


if __name__ == "__main__":
    main()
