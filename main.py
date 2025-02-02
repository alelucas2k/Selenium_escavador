from scraper_facade import ScraperFacade
from database import Database


def main():
    try:
        # Configuração inicial do banco de dados
        db = Database()

        # Cria a tabela se não existir
        db.executar(
            "CREATE TABLE IF NOT EXISTS professores ("
            "id INTEGER PRIMARY KEY, "
            "nome TEXT UNIQUE, "
            "status TEXT DEFAULT 'pendente'"
            ")"
        )

        # Verifica se a coluna 'status' existe
        colunas = db.buscar("PRAGMA table_info(professores)")
        status_existe = any(coluna[1] == 'status' for coluna in colunas)

        if not status_existe:
            db.executar("ALTER TABLE professores ADD COLUMN status TEXT DEFAULT 'pendente'")
            print("Coluna 'status' adicionada ao banco de dados existente.")

        # Lista de professores padrão
        professores = [
            "Victor André Pinho de Oliveira",
            "Paulo Ribeiro Lins Junior",
            "Katyusco Santos",
            "Alexandre Sales Vasconcelos",
            "Marcelo José Siqueira Coutinho de Almeida"
        ]

        # Insere professores no banco (se não existirem)
        for professor in professores:
            try:
                db.executar(
                    "INSERT OR IGNORE INTO professores (nome) VALUES (?)",
                    (professor,)
                )
            except Exception as e:
                print(f"Erro ao inserir professor {professor}: {e}")

        # Cria o scraper
        scraper = ScraperFacade()

        # Processa professores pendentes
        professores_pendentes = db.buscar(
            "SELECT nome FROM professores WHERE status = 'pendente'"
        )

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

    except sqlite3.Error as e:
        print(f"Erro crítico no banco de dados: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        # Garante o fechamento adequado dos recursos
        if 'scraper' in locals():
            scraper.fechar()
        if 'db' in locals():
            db.fechar()
        print("Processo finalizado.")


if __name__ == "__main__":
    main()