
from .Perfil import Perfil

class Professor(Perfil):
    def __init__(self, id, nome, curso, email_institucional, numeroSala, resumo):
        super().__init__(id, nome, curso, email_institucional)  # Chama o construtor da classe pai (Perfil)
        self._numeroSala = numeroSala
        self._areas_interesse = []  # Lista para armazenar as áreas de interesse
        self._projetos = []  # Lista para armazenar os projetos orientados
        self.resumo = resumo

    # Getters
    @property
    def numeroSala(self):
        return self._numeroSala

    @property
    def areas_interesse(self):
        return self._areas_interesse

    @property
    def projetos(self):
        return self._projetos

    # Setters
    @numeroSala.setter
    def numeroSala(self, value):
        self._numeroSala = value

    def add_area_interesse(self, area):
        self._areas_interesse.append(area)

    def add_projeto(self, projeto):
        self._projetos.append(projeto)

    def remove_area_interesse(self, area):
        if area in self._areas_interesse:
            self._areas_interesse.remove(area)

    def remove_projeto(self, projeto):
        if projeto in self._projetos:
            self._projetos.remove(projeto)
#
# # Exemplo de uso
# professor = Professor(id=1, nome="Professor X", curso="Engenharia", email_institucional="professorx@universidade.edu", numeroSala="101")
# print(professor.nome)
# print(professor.numeroSala)
# print(professor.areas_interesse)
# print(professor.projetos)
#
# # Adicionando áreas de interesse e projetos individualmente
# professor.add_area_interesse("Ciência de Dados")
# professor.add_projeto("Projeto A")
#
# print(professor.areas_interesse)
# print(professor.projetos)
#
# # Removendo uma área de interesse e um projeto
# professor.remove_area_interesse("Ciência de Dados")
# professor.remove_projeto("Projeto A")
#
# print(professor.areas_interesse)
# print(professor.projetos)
