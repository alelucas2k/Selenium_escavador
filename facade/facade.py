# main/facade/facade.py

from entity.Aluno import Aluno
from entity.Perfil import Perfil
from entity.ExperienciaProfissional import ExperienciaProfissional
from entity.SugestaoNovoProfessor import SugestaoNovoProfessor
from repository.repository import (
    ProfessorRepository,
    AlunoRepository,
    PerfilRepository,
    ExperienciaProfissionalRepository,
    ProjetoRepository,
    GrandeAreaRepository,
    CursoRepository
)

from datetime import datetime
import psycopg2.errors

from repository.repository import SugestaoNovoProfessorRepository

from entity import Professor


class Facade:

    def inserir_sugestao_professor(self, nome):
        repository = SugestaoNovoProfessorRepository()
        sugestao = SugestaoNovoProfessor(datetime.now().date(), nome)
        repository.add_sugestao(sugestao)


    def apagar_projeto_participado_por_email(self, email, projetos):
        alunoRepository = AlunoRepository()
        aluno = alunoRepository.get_aluno_by_email(email)
        id = aluno[0]

        for projeto in projetos:
            alunoRepository.remove_projeto_from_aluno(id, projeto)


    def inserir_projeto_participado_por_email(self, email, projetos):
        alunoRepository = AlunoRepository()
        aluno = alunoRepository.get_aluno_by_email(email)
        id = aluno[0]

        try:
            for projeto in projetos:
                alunoRepository.add_projeto_to_aluno(id, projeto)
        except psycopg2.errors.UniqueViolation as e:
            print("\nVocê já Participa do projeto. Selecione outro.\n")


    def apagar_area_interesse_por_email(self, email, areas_interesse):
        alunoRepository = AlunoRepository()
        aluno = alunoRepository.get_aluno_by_email(email)
        id = aluno[0]

        for area in areas_interesse:
            alunoRepository.remove_grande_area_from_aluno(id, area)


    def inserir_areas_interesse_por_email(self, email, areas_interesse):
        alunoRepository = AlunoRepository()
        aluno = alunoRepository.get_aluno_by_email(email)
        id = aluno[0]

        try:
            for area in areas_interesse:
                alunoRepository.add_grande_area_to_aluno(id, area)
        except psycopg2.errors.UniqueViolation as e:
            print("\nVocê já demonstrou interesse na área. Selecione outra.\n")


    def apagar_experiencia(self, id):
        repository = ExperienciaProfissionalRepository()
        repository.delete_experiencia(id)


    def update_senha_by_email(self, email, senha):
        repository = AlunoRepository()
        repository.update_senha_by_email(email, senha)


    def update_periodo_by_email(self, email, periodo):
        repository = AlunoRepository()
        repository.update_periodo_by_email(email, periodo)


    def update_curso_by_email(self, email, curso):
        repository = PerfilRepository()
        repository.update_curso_by_email(email, curso)


    def update_nome_by_email(self, email, nome):
        repository = PerfilRepository()
        repository.update_nome_by_email(email, nome)


    def exibir_professores(self):
        repository = ProfessorRepository()
        professores = repository.get_all_professores()

        return professores


    def exibir_aluno(self, email):
        repository = AlunoRepository()
        aluno = repository.get_aluno_by_email(email)
        return aluno


    def exibir_alunos(self, opcao):
        repository = AlunoRepository()
        alunos = repository.get_all_alunos()
        return alunos


    def criar_experiencia_profissional_aluno_by_email(self, email, titulo, data_inicio, data_fim, descricao):
        try:
            self.verifica_datas(data_inicio, data_fim)
            alunoRepository = AlunoRepository()
            aluno = alunoRepository.get_aluno_by_email(email)
            id = aluno[0]
            repository = ExperienciaProfissionalRepository()
            experiencia = ExperienciaProfissional(None, titulo, data_inicio, data_fim, descricao)
            repository.add_experiencia(experiencia, id)
        except ValueError as e:
            print(f"Erro: {e}")


    def criar_experiencia_profissional_aluno(self, id, titulo, data_inicio, data_fim, descricao):
        try:
            self.verifica_datas(data_inicio, data_fim)
            repository = ExperienciaProfissionalRepository()
            experiencia = ExperienciaProfissional(None, titulo, data_inicio, data_fim, descricao)
            repository.add_experiencia(experiencia, id)
        except ValueError as e:
            print(f"Erro: {e}")

    def criar_aluno(self, nome, curso, email_institucional, periodo, senha, experiencias_profissionais, areas_interesse,
                    projetos):
        try:
            self.verifica_email_institucional(email_institucional)
            perfil = Perfil(None, nome, curso, email_institucional)
            repo_perfil = PerfilRepository()
            id_perfil = repo_perfil.add_perfil(perfil)
        except ValueError as e:
            print(f"Erro ao criar aluno: {e}")
            return

        try:
            self.verificar_periodo(periodo)
            self.verificar_senha(senha)
            aluno = Aluno(None, nome, curso, email_institucional, periodo, senha)

            for experiencia in experiencias_profissionais:
                aluno.add_experiencia_profissional(experiencia)
            for area in areas_interesse:
                aluno.add_grande_area(area)
            for projeto in projetos:
                aluno.add_projeto(projeto)

            repo_aluno = AlunoRepository()
            id_aluno = repo_aluno.add_aluno(aluno, id_perfil)
            return id_aluno
        except ValueError as e:
            print(f"Erro ao criar aluno: {e}")
            return


    def criar_professor(self, nome, resumo, areas_interesse, projetos):
        try:
            perfil = Perfil(None, nome, None, None)
            repo_perfil = PerfilRepository()
            id_perfil = repo_perfil.add_perfil(perfil)
        except ValueError as e:
            print(f"Erro ao criar aluno: {e}")
            return

        try:
            professor = Professor(None, nome, None, None, None, resumo)

            for area in areas_interesse:
                professor.add_area_interesse(area)
            for projeto in projetos:
                professor.add_projeto(projeto)

            repo_professor = ProfessorRepository()
            id_professor = repo_professor.add_professor(professor, id_perfil)
            return id_professor
        except ValueError as e:
            print(f"Erro ao criar aluno: {e}")
            return


    def verifica_datas(self, data_inicio, data_fim):
        formato = "%d/%m/%Y"
        data_inicio_dt = datetime.strptime(data_inicio, formato)
        data_fim_dt = datetime.strptime(data_fim, formato)
        if data_inicio_dt > data_fim_dt:
            raise ValueError("Data inicial maior que a data final.")

    def verificar_senha(self, senha):
        if len(senha) < 5:
            raise ValueError("Senha deve ter pelo menos 5 caracteres.")

    def verificar_periodo(self, periodo):
        if not (1 <= int(periodo) <= 10):
            raise ValueError("Período inválido.")

    def verifica_email_institucional(self, email):
        if '@academico.ifpb.edu.br' not in email:
            raise ValueError("Email institucional incorreto.")


    def exibir_projetos(self):
        return ProjetoRepository().get_all_projetos()


    def exibir_areas(self):
        return GrandeAreaRepository().get_all_grande_areas()


    def exibir_cursos(self):
        return CursoRepository().get_all_cursos()
