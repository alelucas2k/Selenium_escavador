from repository import ProfessorRepository

class Observer:
    def update(self, professor, status, resumo=None):
        """
        Método base para atualização dos observadores.
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

class PostgresSummaryUpdater(Observer):
    """
    Observer para atualizar a coluna 'resumo' no PostgreSQL,
    utilizando o método atualizar_resumo_por_nome do ProfessorRepository.
    """
    def __init__(self):
        try:
            self.professor_repo = ProfessorRepository()
        except Exception as e:
            print(f"[ERROR] Falha ao conectar com o repositório PostgreSQL: {e}")

    def update(self, professor, status, resumo=None):
        if status == "resumo gerado" and resumo:
            try:
                # Chama o método que agora atualiza ou insere o professor
                self.professor_repo.atualizar_resumo_por_nome(professor, resumo)
                print(f"[PostgresSummaryUpdater] Resumo de '{professor}' atualizado com sucesso no PostgreSQL.")
            except Exception as e:
                print(f"[ERROR] Falha ao atualizar resumo de '{professor}' no PostgreSQL: {e}")


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
