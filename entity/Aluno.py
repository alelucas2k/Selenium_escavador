from .Perfil import Perfil

class Aluno(Perfil):
    def __init__(self, id, nome, curso, email_institucional, periodo, senha):
        super().__init__(id, nome, curso, email_institucional)  # Chama o construtor da classe pai (Perfil)
        self._periodo = periodo
        self._senha = senha
        self._experiencias_profissionais = []  # Lista para armazenar as experiências profissionais
        self._grande_areas = []  # Lista para armazenar as grandes áreas de interesse
        self._projetos = []  # Lista para armazenar os projetos em que o aluno participa

    # Getters
    @property
    def periodo(self):
        return self._periodo

    @property
    def senha(self):
        return self._senha

    @property
    def experiencias_profissionais(self):
        return self._experiencias_profissionais

    @property
    def grande_areas(self):
        return self._grande_areas

    @property
    def projetos(self):
        return self._projetos

    # Setters
    @periodo.setter
    def periodo(self, value):
        self._periodo = value

    @senha.setter
    def senha(self, value):
        self._senha = value

    def add_experiencia_profissional(self, experiencia):
        self._experiencias_profissionais.append(experiencia)

    def add_grande_area(self, grande_area):
        self._grande_areas.append(grande_area)

    def add_projeto(self, projeto):
        self._projetos.append(projeto)

# # Exemplo de uso
# aluno = Aluno(id=1, nome="João Silva", curso="Ciência da Computação", email_institucional="joao.silva@universidade.edu", periodo="6º período", senha="senha123")
# print(aluno.nome)
# print(aluno.periodo)
# print(aluno.projetos)
#
# # Adicionando experiências profissionais, grandes áreas e projetos individualmente
# aluno.add_experiencia_profissional("Estágio em Desenvolvimento")
# aluno.add_grande_area("Ciências Exatas")
# aluno.add_projeto("Projeto A")
#
# print(aluno.experiencias_profissionais)
# print(aluno.grande_areas)
# print(aluno.projetos)
