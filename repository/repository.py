from repository.singleton.PostgresSingleton import PostgreSQLConnectionSingleton



class Repository:
    def __init__(self):
        # Obtém a conexão usando o Singleton
        self.connection = PostgreSQLConnectionSingleton(database="postgres", user="postgres",
                                                        password="0000", host="localhost",
                                                        port="0000").get_connection()

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


class ProjetoRepository(Repository):

    def get_all_projetos(self):
        query = "SELECT * FROM projeto;"
        return self.fetch_query(query)


    def add_projeto(self, projeto):
        query = ("INSERT INTO projeto (nome, data_inicio, data_fim, "
                 "descricao, eh_pesquisa, eh_extensao) "
                 "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;")
        params = (projeto.nome, projeto.data_inicio, projeto.data_fim, projeto.descricao, projeto.eh_pesquisa, projeto.eh_extensao)
        self.execute_query(query, params)
        projeto.id = self.fetch_query("SELECT LASTVAL();")[0][0]

        # Adicionar associações com grande área
        for grande_area_id in projeto.grande_areas:
            self.add_grande_area_to_projeto(projeto.id, grande_area_id)

    def get_projeto(self, projeto_id):
        query = "SELECT * FROM projeto WHERE id = %s;"
        projeto = self.fetch_query(query, (projeto_id,))
        projeto.grande_areas = self.get_grande_areas_by_projeto(projeto_id)
        return projeto

    def update_projeto(self, projeto):
        query = ("UPDATE projeto SET nome = %s, data_inicio = %s, data_fim = %s,"
                 " descricao = %s, eh_pesquisa = %s, eh_extensao = %s WHERE id = %s;")
        params = (projeto.nome, projeto.data_inicio, projeto.data_fim, projeto.descricao, projeto.eh_pesquisa, projeto.eh_extensao, projeto.id)
        self.execute_query(query, params)

        # Atualizar associações com grande área
        self.clear_grande_areas_from_projeto(projeto.id)
        for grande_area_id in projeto.grande_areas:
            self.add_grande_area_to_projeto(projeto.id, grande_area_id)

    def delete_projeto(self, projeto_id):
        # Remover associações com grandes áreas antes de deletar o projeto
        self.clear_grande_areas_from_projeto(projeto_id)
        query = "DELETE FROM projeto WHERE id = %s;"
        self.execute_query(query, (projeto_id,))

    def add_grande_area_to_projeto(self, projeto_id, grande_area_id):
        query = "INSERT INTO projeto_grande_area (projeto_id, grande_area_id) VALUES (%s, %s);"
        self.execute_query(query, (projeto_id, grande_area_id))

    def clear_grande_areas_from_projeto(self, projeto_id):
        query = "DELETE FROM projeto_grande_area WHERE projeto_id = %s;"
        self.execute_query(query, (projeto_id,))

    def get_grande_areas_by_projeto(self, projeto_id):
        query = "SELECT grande_area_id FROM projeto_grande_area WHERE projeto_id = %s;"
        return [row[0] for row in self.fetch_query(query, (projeto_id,))]


class SugestaoNovoProfessorRepository(Repository):
    def add_sugestao(self, sugestao):
        query = ("INSERT INTO sugestao_novo_professor (data_sugestao, nome_professor)"
                 " VALUES (%s, %s) RETURNING id;")
        params = (sugestao.data_sugestao, sugestao.nome_professor)
        self.execute_query(query, params)
        sugestao.id = self.fetch_query("SELECT LASTVAL();")[0][0]

    def get_sugestao(self, sugestao_id):
        query = "SELECT * FROM sugestao_novo_professor WHERE id = %s;"
        return self.fetch_query(query, (sugestao_id,))

    def update_sugestao(self, sugestao):
        query = "UPDATE sugestao_novo_professor SET data_sugestao = %s, nome_professor = %s WHERE id = %s;"
        params = (sugestao.data_sugestao, sugestao.nome_professor, sugestao.id)
        self.execute_query(query, params)

    def delete_sugestao(self, sugestao_id):
        query = "DELETE FROM sugestao_novo_professor WHERE id = %s;"
        self.execute_query(query, (sugestao_id,))


class SugestaoMelhoriaRepository(Repository):
    def add_sugestao(self, sugestao):
        query = "INSERT INTO sugestao_melhoria (data_sugestao, sugestao) VALUES (%s, %s) RETURNING id;"
        params = (sugestao.data_sugestao, sugestao.sugestao)
        self.execute_query(query, params)
        sugestao.id = self.fetch_query("SELECT LASTVAL();")[0][0]

    def get_sugestao(self, sugestao_id):
        query = "SELECT * FROM sugestao_melhoria WHERE id = %s;"
        return self.fetch_query(query, (sugestao_id,))

    def update_sugestao(self, sugestao):
        query = "UPDATE sugestao_melhoria SET data_sugestao = %s, sugestao = %s WHERE id = %s;"
        params = (sugestao.data_sugestao, sugestao.sugestao, sugestao.id)
        self.execute_query(query, params)

    def delete_sugestao(self, sugestao_id):
        query = "DELETE FROM sugestao_melhoria WHERE id = %s;"
        self.execute_query(query, (sugestao_id,))


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

class GrandeAreaRepository(Repository):
    def add_grande_area(self, grande_area):
        query = "INSERT INTO grande_area (area) VALUES (%s) RETURNING id;"
        params = (grande_area.area,)
        self.execute_query(query, params)
        grande_area.id = self.fetch_query("SELECT LASTVAL();")[0][0]

    def get_grande_area(self, grande_area_id):
        query = "SELECT * FROM grande_area WHERE id = %s;"
        return self.fetch_query(query, (grande_area_id,))

    def update_grande_area(self, grande_area):
        query = "UPDATE grande_area SET area = %s WHERE id = %s;"
        params = (grande_area.area, grande_area.id)
        self.execute_query(query, params)

    def delete_grande_area(self, grande_area_id):
        query = "DELETE FROM grande_area WHERE id = %s;"
        self.execute_query(query, (grande_area_id,))

    def get_projetos_by_grande_area(self, grande_area_id):
        query = ("SELECT p.* FROM projeto p "
                 "JOIN projeto_grande_area pga ON p.id = pga.projeto_id "
                 "WHERE pga.grande_area_id = %s;")
        return self.fetch_query(query, (grande_area_id,))

    def get_professores_by_grande_area(self, grande_area_id):
        query = ("SELECT pr.* FROM professor pr "
                 "JOIN professor_grande_area pga ON pr.id = pga.professor_id "
                 "WHERE pga.grande_area_id = %s;")
        return self.fetch_query(query, (grande_area_id,))

    def get_alunos_by_grande_area(self, grande_area_id):
        query = ("SELECT a.* FROM aluno a "
                 "JOIN aluno_grande_area aga ON a.id = aga.aluno_id "
                 "WHERE aga.grande_area_id = %s;")
        return self.fetch_query(query, (grande_area_id,))

    def get_all_grande_areas(self):
        query = "SELECT * FROM grande_area;"
        return self.fetch_query(query)


class ExperienciaProfissionalRepository(Repository):
    def add_experiencia(self, experiencia, id):
        query = ("INSERT INTO experiencia_profissional "
                 "(id_aluno, titulo, data_inicio, data_fim, descricao) VALUES (%s, %s, %s, %s, %s) RETURNING id;")
        params = (id, experiencia.titulo, experiencia.dataInicio, experiencia.dataFim, experiencia.descricao)
        self.execute_query(query, params)
        experiencia.id = self.fetch_query("SELECT LASTVAL();")[0][0]

    def get_experiencia(self, experiencia_id):
        query = "SELECT * FROM experiencia_profissional WHERE id = %s;"
        return self.fetch_query(query, (experiencia_id,))

    def update_experiencia(self, experiencia):
        query = ("UPDATE experiencia_profissional SET "
                 "titulo = %s, data_inicio = %s, data_fim = %s, descricao = %s WHERE id = %s;")
        params = (experiencia.titulo, experiencia.dataInicio, experiencia.dataFim, experiencia.descricao, experiencia.id)
        self.execute_query(query, params)

    def delete_experiencia(self, experiencia_id):
        query = "DELETE FROM experiencia_profissional WHERE id = %s;"
        self.execute_query(query, (experiencia_id,))

# CREATE TABLE aluno_projeto (
#     aluno_id INT REFERENCES aluno(id),
#     projeto_id INT REFERENCES projeto(id),
#     PRIMARY KEY (aluno_id, projeto_id)
# );
class AlunoRepository(PerfilRepository):
    def __init__(self):
        super().__init__()
        self.experiencia_profissional_repository = ExperienciaProfissionalRepository()

    def add_aluno(self, aluno, id_perfil):
        # Depois, adiciona os dados específicos do aluno
        query = "INSERT INTO aluno (id_perfil, periodo, senha) VALUES (%s, %s, %s);"
        params = (id_perfil, aluno.periodo, aluno.senha)
        self.execute_query(query, params)
        aluno.id = self.fetch_query("SELECT LASTVAL();")[0][0]

        # Adiciona as experiências profissionais do aluno
        for experiencia in aluno.experiencias_profissionais:
            experiencia.id_perfil = aluno.id
            self.experiencia_profissional_repository.add_experiencia(experiencia, aluno.id)

        # Adicionar interesses em grandes áreas
        for grande_area_id in aluno.grande_areas:
            self.add_grande_area_to_aluno(aluno.id, grande_area_id)

        # Adicionar participação em projetos
        for projeto_id in aluno.projetos:
            self.add_projeto_to_aluno(aluno.id, projeto_id)

        return aluno.id

    def get_aluno_by_email(self, email):
        query = ("SELECT a.id, p.nome, p.curso, p.email_institucional, a.periodo, a.senha, "
                 "ARRAY(SELECT row_to_json(ep) FROM (SELECT ep.titulo, ep.data_inicio, ep.data_fim, ep.descricao, ep.id FROM experiencia_profissional ep WHERE ep.id_aluno = a.id) ep) AS experiencias_profissionais, "
                 "ARRAY(SELECT ga.area FROM aluno_grande_area aga "
                 "JOIN grande_area ga ON aga.grande_area_id = ga.id "
                 "WHERE aga.aluno_id = a.id) AS grande_areas, "
                 "ARRAY(SELECT pj.nome FROM aluno_projeto ap "
                 "JOIN projeto pj ON ap.projeto_id = pj.id "
                 "WHERE ap.aluno_id = a.id) AS projetos "
                 "FROM aluno a "
                 "JOIN perfil p ON a.id_perfil = p.id "
                 "WHERE p.email_institucional = %s;")
        resultado = self.fetch_query(query, (email,))
        return resultado[0] if resultado else None

    def get_aluno(self, aluno_id):
        # Obtém os dados do perfil
        perfil_data = self.get_perfil(aluno_id)
        # Obtém os dados específicos do aluno
        query = "SELECT periodo, senha FROM aluno WHERE id_perfil = %s;"
        aluno_data = self.fetch_query(query, (aluno_id,))

        # Obtém as experiências profissionais do aluno
        query = "SELECT * FROM experiencia_profissional WHERE id_aluno = %s;"
        experiencias_data = self.fetch_query(query, (aluno_id,))

        # Obtém os interesses em grandes áreas
        query = ("SELECT ga.area FROM aluno_grande_area aga "
                 "JOIN grande_area ga ON aga.grande_area_id = ga.id "
                 "WHERE aga.aluno_id = %s;")
        grande_areas = [row[0] for row in self.fetch_query(query, (aluno_id,))]

        # Obtém a participação em projetos
        query = ("SELECT p.nome FROM aluno_projeto ap "
                 "JOIN projeto p ON ap.projeto_id = p.id "
                 "WHERE ap.aluno_id = %s;")
        projetos = [row[0] for row in self.fetch_query(query, (aluno_id,))]

        return perfil_data + aluno_data + experiencias_data + grande_areas + projetos

    def update_aluno(self, aluno):
        # Atualiza os dados do perfil
        self.update_perfil(aluno)
        # Atualiza os dados específicos do aluno
        query = "UPDATE aluno SET periodo = %s, senha = %s WHERE id_perfil = %s;"
        params = (aluno.periodo, aluno.senha, aluno.id)
        self.execute_query(query, params)

        # Atualiza as experiências profissionais do aluno
        for experiencia in aluno.experiencias_profissionais:
            self.experiencia_profissional_repository.update_experiencia(experiencia)

        # Atualiza interesses em grandes áreas
        self.clear_grande_areas_from_aluno(aluno.id)
        for grande_area_id in aluno.grande_areas:
            self.add_grande_area_to_aluno(aluno.id, grande_area_id)

        # Atualiza participação em projetos
        self.clear_projetos_from_aluno(aluno.id)
        for projeto_id in aluno.projetos:
            self.add_projeto_to_aluno(aluno.id, projeto_id)

    def delete_aluno(self, aluno_id):
        # Deleta as experiências profissionais do aluno
        query = "DELETE FROM experiencia_profissional WHERE id_perfil = %s;"
        self.execute_query(query, (aluno_id,))
        # Deleta os interesses em grandes áreas
        self.clear_grande_areas_from_aluno(aluno_id)
        # Deleta a participação em projetos
        self.clear_projetos_from_aluno(aluno_id)
        # Deleta os dados específicos do aluno
        query = "DELETE FROM aluno WHERE id_perfil = %s;"
        self.execute_query(query, (aluno_id,))
        # Deleta os dados do perfil
        self.delete_perfil(aluno_id)

    def add_grande_area_to_aluno(self, aluno_id, grande_area_id):
        query = "INSERT INTO aluno_grande_area (aluno_id, grande_area_id) VALUES (%s, %s);"
        self.execute_query(query, (aluno_id, grande_area_id))

    def clear_grande_areas_from_aluno(self, aluno_id):
        query = "DELETE FROM aluno_grande_area WHERE aluno_id = %s;"
        self.execute_query(query, (aluno_id,))

    def remove_grande_area_from_aluno(self, aluno_id, grande_area_id):
        query = "DELETE FROM aluno_grande_area WHERE aluno_id = %s AND grande_area_id = %s;"
        self.execute_query(query, (aluno_id, grande_area_id))

    def add_projeto_to_aluno(self, aluno_id, projeto_id):
        query = "INSERT INTO aluno_projeto (aluno_id, projeto_id) VALUES (%s, %s);"
        self.execute_query(query, (aluno_id, projeto_id))

    def remove_projeto_from_aluno(self, aluno_id, projeto_id):
        query = "DELETE FROM aluno_projeto WHERE aluno_id = %s AND projeto_id = %s;"
        self.execute_query(query, (aluno_id, projeto_id))

    def get_all_alunos(self):
        query = ("SELECT a.id, p.nome, p.curso, p.email_institucional, a.periodo, a.senha, "
                 "ARRAY(SELECT row_to_json(ep) FROM (SELECT ep.titulo, ep.data_inicio, ep.data_fim, ep.descricao, ep.id FROM experiencia_profissional ep WHERE ep.id_aluno = a.id) ep) AS experiencias_profissionais, "
                 "ARRAY(SELECT ga.area FROM aluno_grande_area aga "
                 "JOIN grande_area ga ON aga.grande_area_id = ga.id "
                 "WHERE aga.aluno_id = a.id) AS grande_areas, "
                 "ARRAY(SELECT pj.nome FROM aluno_projeto ap "
                 "JOIN projeto pj ON ap.projeto_id = pj.id "
                 "WHERE ap.aluno_id = a.id) AS projetos "
                 "FROM aluno a "
                 "JOIN perfil p ON a.id_perfil = p.id;")
        return self.fetch_query(query)

    def get_alunos_by_grande_area(self, grande_area_id):
        query = ("SELECT p.id, p.nome, p.curso, p.email_institucional, a.periodo, a.senha, "
                 "ARRAY(SELECT ep.titulo FROM experiencia_profissional ep WHERE ep.id_perfil = p.id) AS experiencias_profissionais, "
                 "ARRAY(SELECT ga.area FROM aluno_grande_area aga "
                 "JOIN grande_area ga ON aga.grande_area_id = ga.id "
                 "WHERE aga.aluno_id = a.id) AS grande_areas, "
                 "ARRAY(SELECT pj.nome FROM aluno_projeto ap "
                 "JOIN projeto pj ON ap.projeto_id = pj.id "
                 "WHERE ap.aluno_id = a.id) AS projetos "
                 "FROM aluno a "
                 "JOIN perfil p ON a.id_perfil = p.id "
                 "JOIN aluno_grande_area aga ON a.id = aga.aluno_id "
                 "WHERE aga.grande_area_id = %s;")
        return self.fetch_query(query, (grande_area_id,))

    def update_periodo_by_email(self, email, periodo):
        query = ("UPDATE aluno SET periodo = %s "
                 "FROM perfil "
                 "WHERE aluno.id_perfil = perfil.id "
                 "AND perfil.email_institucional = %s;")
        self.execute_query(query, (periodo, email))

    def update_senha_by_email(self, email, senha):
        query = ("UPDATE aluno SET senha = %s "
                 "FROM perfil "
                 "WHERE aluno.id_perfil = perfil.id "
                 "AND perfil.email_institucional = %s;")
        self.execute_query(query, (senha, email))

# CREATE TABLE professor_projeto (
#     professor_id INT REFERENCES professor(id),
#     projeto_id INT REFERENCES projeto(id),
#     PRIMARY KEY (professor_id, projeto_id)
# );

class CursoRepository(Repository):
    def get_all_cursos(self):
        query = "SELECT * FROM curso;"
        return self.fetch_query(query)


class ProfessorRepository(PerfilRepository):
    def add_professor(self, professor, id_perfil):
        # Adiciona os dados específicos do professor
        query = "INSERT INTO professor (id_perfil, resumo) VALUES (%s, %s);"
        params = (id_perfil, professor.resumo)
        self.execute_query(query, params)
        professor.id = self.fetch_query("SELECT LASTVAL();")[0][0]

        # Adiciona as áreas de interesse do professor
        for area in professor._areas_interesse:
            self.add_grande_area_to_professor(professor.id, area)

        # Adiciona participação em projetos
        for projeto_id in professor._projetos:
            self.add_projeto_to_professor(professor.id, projeto_id)

        return professor.id

    def get_professor(self, professor_id):
        # Obtém os dados do perfil
        perfil_data = self.get_perfil(professor_id)
        # Obtém os dados específicos do professor
        query = "SELECT numero_sala FROM professor WHERE id = %s;"
        professor_data = self.fetch_query(query, (professor_id,))

        # Obtém os interesses em grandes áreas
        query = ("SELECT ga.area FROM professor_grande_area pga "
                 "JOIN grande_area ga ON pga.grande_area_id = ga.id "
                 "WHERE pga.professor_id = %s;")
        grande_areas = [row[0] for row in self.fetch_query(query, (professor_id,))]

        # Obtém os projetos orientados
        query = "SELECT projeto_id FROM professor_projeto WHERE professor_id = %s;"
        projetos_orientados = [row[0] for row in self.fetch_query(query, (professor_id,))]

        return perfil_data + professor_data + grande_areas + projetos_orientados

    def update_professor(self, professor):
        # Atualiza os dados do perfil
        self.update_perfil(professor)
        # Atualiza os dados específicos do professor
        query = "UPDATE professor SET numero_sala = %s WHERE id = %s;"
        params = (professor.numeroSala, professor.id)
        self.execute_query(query, params)

        # Atualiza interesses em grandes áreas
        self.clear_grande_areas_from_professor(professor.id)
        for grande_area_id in professor.grande_areas:
            self.add_grande_area_to_professor(professor.id, grande_area_id)

        # Atualiza orientação de projetos
        self.clear_projetos_from_professor(professor.id)
        for projeto_id in professor.projetos_orientados:
            self.add_projeto_to_professor(professor.id, projeto_id)

    def delete_professor(self, professor_id):
        # Deleta os interesses em grandes áreas
        self.clear_grande_areas_from_professor(professor_id)
        # Deleta orientação de projetos
        self.clear_projetos_from_professor(professor_id)
        # Deleta os dados específicos do professor
        query = "DELETE FROM professor WHERE id = %s;"
        self.execute_query(query, (professor_id,))
        # Deleta os dados do perfil
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
        query = ("SELECT p.id, p.nome, pr.resumo, " 
                 "ARRAY(SELECT ga.area FROM professor_grande_area pga " 
                 "JOIN grande_area ga ON pga.grande_area_id = ga.id "
                 "WHERE pga.professor_id = pr.id) AS grande_areas, " 
                 "ARRAY(SELECT pj.nome FROM professor_projeto pp " 
                 "JOIN projeto pj ON pp.projeto_id = pj.id " 
                 "WHERE pp.professor_id = pr.id) AS projetos_orientados "
                 "FROM professor pr " 
                 "JOIN perfil p ON pr.id_perfil = p.id;")
        return self.fetch_query(query)

    # talvez precise corrigir o pr.id ver dps
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

