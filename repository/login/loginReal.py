from repository.repositories import (
    AlunoRepository
)
from repository.login.loginInterface import LoginInterface


class LoginReal(LoginInterface):
    def autenticar(self, email, senha):
        aluno_repo = AlunoRepository()

        # Verifica se o usuário é um aluno
        aluno = aluno_repo.fetch_query(
            "SELECT p.id, p.nome, p.curso, p.email_institucional, a.periodo, a.senha, "
            "ARRAY(SELECT row_to_json(ep) FROM (SELECT ep.titulo, ep.data_inicio, ep.data_fim, ep.descricao FROM experiencia_profissional ep WHERE ep.id_aluno = a.id) ep) AS experiencias_profissionais, "
            "ARRAY(SELECT ga.area FROM aluno_grande_area aga "
            "JOIN grande_area ga ON aga.grande_area_id = ga.id "
            "WHERE aga.aluno_id = a.id) AS grande_areas, "
            "ARRAY(SELECT pj.nome FROM aluno_projeto ap "
            "JOIN projeto pj ON ap.projeto_id = pj.id "
            "WHERE ap.aluno_id = a.id) AS projetos "
            "FROM aluno a "
            "JOIN perfil p ON a.id_perfil = p.id "
            "WHERE p.email_institucional = %s AND a.senha = %s;",
            (email, senha)
        )

        if aluno:
            return {"status": "success", "tipo": "aluno", "dados": aluno[0]}

        return {"status": "fail", "message": "Credenciais inválidas"}
