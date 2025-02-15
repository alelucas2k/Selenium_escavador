from repository import ProfessorRepository

class Observer:
    def update(self, professor, status, resumo=None):
        """
        Metodo base para atualização dos observadores.
        """
        pass

class StatusLogger(Observer):
    def update(self, professor, status, resumo=None):
        """
        Loga o status do professor no console.
        """
        print(f"[LOG] {professor} -> {status}")
        if resumo:
            print(f"[LOG] Resumo atualizado para {professor}")

# class PostgresSummaryUpdater(Observer):
#     """
#     Observer para atualizar a coluna 'resumo' no PostgreSQL,
#     utilizando o método atualizar_resumo_por_nome do ProfessorRepository.
#     """
#     def __init__(self):
#         try:
#             self.professor_repo = ProfessorRepository()
#         except Exception as e:
#             print(f"[ERROR] Falha ao conectar com o repositório PostgreSQL: {e}")

#     def update(self, professor, status, resumo=None):
#         if status == "resumo gerado" and resumo:
#             try:
#                 # Chama o método que agora atualiza ou insere o professor
#                 self.professor_repo.atualizar_resumo_por_nome(professor, resumo)
#                 print(f"[PostgresSummaryUpdater] Resumo de '{professor}' atualizado com sucesso no PostgreSQL.")
#             except Exception as e:
#                 print(f"[ERROR] Falha ao atualizar resumo de '{professor}' no PostgreSQL: {e}")


class PostgresSummaryUpdater(Observer):
    def __init__(self):
        try:
            self.professor_repo = ProfessorRepository()
        except Exception as e:
            print(f"[ERROR] Falha ao conectar com o repositório PostgreSQL: {e}")
            self.professor_repo = None

    def update(self, professor, status, info=None):
        if status == "resumo gerado" and info:
            resumo = info.get("resumo")
            area = info.get("area")
            projetos = info.get("projetos")
            if not self.professor_repo:
                print(f"[ERROR] Repositório não disponível para atualizar {professor}.")
                return
            try:
                # Atualiza o resumo na tabela professor
                self.professor_repo.atualizar_resumo_por_nome(professor, resumo)

                # Atualiza a área de atuação na tabela professor_grande_area
                self.professor_repo.clear_grande_areas_from_professor_by_nome(professor)
                self.professor_repo.add_grande_area_to_professor_por_nome(professor, area)

                # Atualiza os projetos na tabela professor_projeto
                self.professor_repo.clear_projetos_from_professor_by_nome(professor)
                for proj in projetos:
                    self.professor_repo.add_projeto_to_professor_por_nome(professor, proj)

                print(f"[PostgresSummaryUpdater] Dados atualizados para '{professor}'.")
            except Exception as e:
                print(f"[ERROR] Falha ao atualizar dados de '{professor}': {e}")

class Subject:
    def __init__(self):
        """
        Inicializa o Subject com uma lista vazia de observadores.
        """
        self._observers = []

    def adicionar_observador(self, observer):
        """
        Adiciona um observador à lista de observadores.
        """
        self._observers.append(observer)

    def notificar(self, professor, status, resumo=None):
        """
        Notifica todos os observadores sobre uma mudança de status.
        """
        for observer in self._observers:
            observer.update(professor, status, resumo)
