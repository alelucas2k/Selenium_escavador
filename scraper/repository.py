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
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(1, 20,
                                                                      user=user,
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

class Repository:
    def __init__(self):
        # Obtém a conexão usando o Singleton
        self.connection = PostgreSQLConnectionSingleton(database="postgres",
                                                        user="postgres",
                                                        password="4667",
                                                        host="localhost",
                                                        port="5432").get_connection()

    def close_connection(self):
        if self.connection:
            PostgreSQLConnectionSingleton().return_connection(self.connection)
            self.connection = None

    def execute_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()

    def fetch_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def __del__(self):
        self.close_connection()

class PerfilRepository(Repository):
    def add_perfil(self, perfil):
        query = "INSERT INTO perfil (nome, curso, email_institucional) VALUES (%s, %s, %s) RETURNING id;"
        params = (perfil.nome, perfil.curso, perfil.email_institucional)
        self.execute_query(query, params)
        perfil.id = self.fetch_query("SELECT LASTVAL();")[0][0]
        return perfil.id

    def get_perfil(self, perfil_id):
        query = "SELECT * FROM perfil WHERE id = %s;"
        return self.fetch_query(query, (perfil_id,))

    def update_curso_by_email(self, email, curso):
        query = "UPDATE perfil SET curso = %s WHERE email_institucional = %s;"
        self.execute_query(query, (curso, email))

    def update_nome_by_email(self, email, novo_nome):
        query = "UPDATE perfil SET nome = %s WHERE email_institucional = %s;"
        self.execute_query(query, (novo_nome, email))

    def update_perfil(self, perfil):
        query = "UPDATE perfil SET nome = %s, curso = %s, email_institucional = %s WHERE id = %s;"
        params = (perfil.nome, perfil.curso, perfil.email_institucional, perfil.id)
        self.execute_query(query, params)

    def delete_perfil(self, perfil_id):
        query = "DELETE FROM perfil WHERE id = %s;"
        self.execute_query(query, (perfil_id,))

class ProfessorRepository(PerfilRepository):

    def atualizar_resumo_por_nome(self, nome_professor, novo_resumo):
        query_update = """
            UPDATE professor
            SET resumo = %s
            FROM perfil
            WHERE professor.id_perfil = perfil.id
              AND perfil.nome = %s;
        """
        params_update = (novo_resumo, nome_professor)
        with self.connection.cursor() as cursor:
            cursor.execute(query_update, params_update)
            self.connection.commit()
            if cursor.rowcount == 0:
                print(f"[ProfessorRepository] Professor '{nome_professor}' não encontrado, criando novo registro.")
                # Insere o novo perfil com email fictício e obtém seu ID
                query_insert_perfil = """
                    INSERT INTO perfil (nome, email_institucional)
                    VALUES (%s, %s)
                    RETURNING id;
                """
                email_ficticio = "professor@academico.ifpb.edu.br"
                cursor.execute(query_insert_perfil, (nome_professor, email_ficticio))
                perfil_id = cursor.fetchone()[0]
                # Insere na tabela professor com o resumo e um número de sala default (por exemplo, 0)
                query_insert_professor = """
                    INSERT INTO professor (id_perfil, resumo, numero_sala)
                    VALUES (%s, %s, %s);
                """
                default_numero_sala = 0  # ou outro número de sua escolha
                cursor.execute(query_insert_professor, (perfil_id, novo_resumo, default_numero_sala))
                self.connection.commit()
                print(f"[ProfessorRepository] Novo professor '{nome_professor}' criado com sucesso.")

    def obtem_id_professor_por_nome(self, nome_professor):
        """
        Retorna o ID da tabela professor, relacionando com a tabela perfil pelo nome.
        """
        query = """
            SELECT prof.id
            FROM professor AS prof
            JOIN perfil ON prof.id_perfil = perfil.id
            WHERE perfil.nome = %s;
        """
        result = self.fetch_query(query, (nome_professor,))
        return result[0][0] if result else None

    def add_professor(self, professor, id_perfil):
        query = "INSERT INTO professor (id_perfil, resumo) VALUES (%s, %s);"
        params = (id_perfil, professor.resumo)
        self.execute_query(query, params)
        professor.id = self.fetch_query("SELECT LASTVAL();")[0][0]
        for area in professor._areas_interesse:
            self.add_grande_area_to_professor(professor.id, area)
        for projeto_id in professor._projetos:
            self.add_projeto_to_professor(professor.id, projeto_id)
        return professor.id

    def get_professor(self, professor_id):
        perfil_data = self.get_perfil(professor_id)
        query = "SELECT numero_sala FROM professor WHERE id = %s;"
        professor_data = self.fetch_query(query, (professor_id,))
        query = ("SELECT ga.area FROM professor_grande_area pga "
                 "JOIN grande_area ga ON pga.grande_area_id = ga.id "
                 "WHERE pga.professor_id = %s;")
        grande_areas = [row[0] for row in self.fetch_query(query, (professor_id,))]
        query = "SELECT projeto_id FROM professor_projeto WHERE professor_id = %s;"
        projetos_orientados = [row[0] for row in self.fetch_query(query, (professor_id,))]
        return perfil_data + professor_data + grande_areas + projetos_orientados

    def update_professor(self, professor):
        self.update_perfil(professor)
        query = "UPDATE professor SET numero_sala = %s WHERE id = %s;"
        params = (professor.numeroSala, professor.id)
        self.execute_query(query, params)
        self.clear_grande_areas_from_professor(professor.id)
        for grande_area_id in professor.grande_areas:
            self.add_grande_area_to_professor(professor.id, grande_area_id)
        self.clear_projetos_from_professor(professor.id)
        for projeto_id in professor.projetos_orientados:
            self.add_projeto_to_professor(professor.id, projeto_id)

    def delete_professor(self, professor_id):
        self.clear_grande_areas_from_professor(professor_id)
        self.clear_projetos_from_professor(professor_id)
        query = "DELETE FROM professor WHERE id = %s;"
        self.execute_query(query, (professor_id,))
        self.delete_perfil(professor_id)

    def add_grande_area_to_professor(self, professor_id, grande_area_id):
        query = "INSERT INTO professor_grande_area (professor_id, grande_area_id) VALUES (%s, %s);"
        self.execute_query(query, (professor_id, grande_area_id))

    def clear_grande_areas_from_professor(self, professor_id):
        query = "DELETE FROM professor_grande_area WHERE professor_id = %s;"
        self.execute_query(query, (professor_id,))

    def add_projeto_to_professor(self, professor_id, projeto_id):
        query = "INSERT INTO professor_projeto (professor_id, projeto_id) VALUES (%s, %s);"
        self.execute_query(query, (professor_id, projeto_id))

    def clear_projetos_from_professor(self, professor_id):
        query = "DELETE FROM professor_projeto WHERE professor_id = %s;"
        self.execute_query(query, (professor_id,))

    def remove_projeto_from_professor(self, professor_id, projeto_id):
        query = "DELETE FROM professor_projeto WHERE professor_id = %s AND projeto_id = %s;"
        self.execute_query(query, (professor_id, projeto_id))

    def remove_grande_area_from_professor(self, professor_id, grande_area_id):
        query = "DELETE FROM professor_grande_area WHERE professor_id = %s AND grande_area_id = %s;"
        self.execute_query(query, (professor_id, grande_area_id))

    def get_all_professores(self):
        query = ("SELECT p.id, p.nome, p.curso, p.email_institucional, pr.numero_sala, " 
                 "ARRAY(SELECT ga.area FROM professor_grande_area pga " 
                 "JOIN grande_area ga ON pga.grande_area_id = ga.id "
                 "WHERE pga.professor_id = pr.id) AS grande_areas, " 
                 "ARRAY(SELECT pj.nome FROM professor_projeto pp " 
                 "JOIN projeto pj ON pp.projeto_id = pj.id " 
                 "WHERE pp.professor_id = pr.id) AS projetos_orientados "
                 "FROM professor pr " 
                 "JOIN perfil p ON pr.id_perfil = p.id;")
        return self.fetch_query(query)

    def get_professores_by_grande_area(self, grande_area_id):
        query = ("SELECT p.id, p.nome, p.curso, p.email_institucional, pr.numero_sala, " 
                 "ARRAY(SELECT ga.area FROM professor_grande_area pga " 
                 "JOIN grande_area ga ON pga.grande_area_id = ga.id "
                 "WHERE pga.professor_id = pr.id) AS grande_areas, " 
                 "ARRAY(SELECT pj.nome FROM professor_projeto pp " 
                 "JOIN projeto pj ON pp.projeto_id = pj.id " 
                 "WHERE pp.professor_id = pr.id) AS projetos_orientados "
                 "FROM professor pr " 
                 "JOIN perfil p ON pr.id_perfil = p.id " 
                 "JOIN professor_grande_area pga ON pr.id_perfil = pga.professor_id " 
                 "WHERE pga.grande_area_id = %s;")
        return self.fetch_query(query, (grande_area_id,))

    # ====================== Métodos Adicionais para Atualizações Usando o Nome ======================

    def get_grande_area_id(self, area_text):
        """
        Obtém o ID de uma grande área a partir do nome. Se não existir, cria um novo registro.
        """
        query = "SELECT id FROM grande_area WHERE area = %s;"
        result = self.fetch_query(query, (area_text,))
        if result:
            return result[0][0]
        else:
            query_insert = "INSERT INTO grande_area (area) VALUES (%s) RETURNING id;"
            self.execute_query(query_insert, (area_text,))
            new_id = self.fetch_query("SELECT LASTVAL();")[0][0]
            return new_id

    def get_projeto_id(self, projeto_title):
        """
        Obtém o ID de um projeto a partir do título. Se não existir, cria um novo projeto com dados mínimos.
        """
        query = "SELECT id FROM projeto WHERE nome = %s;"
        result = self.fetch_query(query, (projeto_title,))
        if result:
            return result[0][0]
        else:
            # Cria um novo projeto com data_inicio como a data atual e placeholders para outros campos.
            query_insert = "INSERT INTO projeto (nome, data_inicio, eh_pesquisa, eh_extensao) VALUES (%s, CURRENT_DATE, false, false) RETURNING id;"
            self.execute_query(query_insert, (projeto_title,))
            new_id = self.fetch_query("SELECT LASTVAL();")[0][0]
            return new_id

    def clear_grande_areas_from_professor_by_nome(self, nome_professor):
        professor_id = self.obtem_id_professor_por_nome(nome_professor)
        if professor_id:
            self.clear_grande_areas_from_professor(professor_id)
        else:
            print(f"Professor '{nome_professor}' não encontrado para limpar grandes áreas.")

    def add_grande_area_to_professor_por_nome(self, nome_professor, area_text):
        professor_id = self.obtem_id_professor_por_nome(nome_professor)
        if professor_id:
            area_id = self.get_grande_area_id(area_text)
            self.add_grande_area_to_professor(professor_id, area_id)
        else:
            print(f"Professor '{nome_professor}' não encontrado para adicionar grande área.")

    def clear_projetos_from_professor_by_nome(self, nome_professor):
        professor_id = self.obtem_id_professor_por_nome(nome_professor)
        if professor_id:
            self.clear_projetos_from_professor(professor_id)
        else:
            print(f"Professor '{nome_professor}' não encontrado para limpar projetos.")

    def add_projeto_to_professor_por_nome(self, nome_professor, projeto_title):
        professor_id = self.obtem_id_professor_por_nome(nome_professor)
        if professor_id:
            projeto_id = self.get_projeto_id(projeto_title)
            self.add_projeto_to_professor(professor_id, projeto_id)
        else:
            print(f"Professor '{nome_professor}' não encontrado para adicionar projeto.")
