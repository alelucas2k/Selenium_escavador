"""
Padrão utilizado: Observer.
Explicação:
Implementa o padrão Observer para notificar múltiplos componentes (como loggers e atualizadores de banco de dados)
sobre as mudanças de status dos professores. Essa abordagem desacoplada facilita a extensão e a manutenção dos comportamentos reativos.
"""


from database import Database  # Certifique-se de que a importação está correta

class Observer:
    def update(self, professor, status, resumo=None):  # Adicionado resumo como argumento opcional
        """
        Metodo base para atualização dos observadores.
        Pode ser sobrescrito pelas subclasses para implementar comportamentos específicos.

        Parâmetros:
            professor (str): Nome do professor.
            status (str): Status atual do professor (ex: "encontrado", "resumo gerado").
            resumo (str, opcional): Resumo do currículo, se disponível.
        """
        pass

class StatusLogger(Observer):
    def update(self, professor, status, resumo=None):  # Adicionado resumo como argumento opcional
        """
        Loga o status do professor no console.
        Se um resumo for fornecido, ele também será exibido.

        Parâmetros:
            professor (str): Nome do professor.
            status (str): Status atual do professor.
            resumo (str, opcional): Resumo do currículo, se disponível.
        """
        if resumo:
            print(f"[LOG] {professor} -> {status}")
        else:
            print(f"[LOG] {professor} -> {status}")

class StatusDatabaseUpdater(Observer):
    def update(self, professor, status, resumo=None):  # Adicionado resumo como argumento opcional
        """
        Atualiza o status do professor no banco de dados.
        Se um resumo for fornecido, ele também será salvo.

        Parâmetros:
            professor (str): Nome do professor.
            status (str): Status atual do professor.
            resumo (str, opcional): Resumo do currículo, se disponível.
        """
        db = Database()
        if status == "resumo gerado" and resumo:
            # Atualiza o status e o resumo no banco de dados
            db.executar("UPDATE professores SET status = ?, resumo = ? WHERE nome = ?", 
                        (status, resumo, professor))
        else:
            # Atualiza apenas o status no banco de dados
            db.executar("UPDATE professores SET status = ? WHERE nome = ?", (status, professor))

class Subject:
    def __init__(self):
        """
        Inicializa o Subject com uma lista vazia de observadores.
        """
        self._observers = []

    def adicionar_observador(self, observer):
        """
        Adiciona um observador à lista de observadores.

        Parâmetros:
            observer (Observer): Instância de um observador.
        """
        self._observers.append(observer)

    def notificar(self, professor, status, resumo=None):  # Adicionado resumo como argumento opcional
        """
        Notifica todos os observadores sobre uma mudança de status.
        Se um resumo for fornecido, ele também será passado aos observadores.

        Parâmetros:
            professor (str): Nome do professor.
            status (str): Status atual do professor.
            resumo (str, opcional): Resumo do currículo, se disponível.
        """
        for observer in self._observers:
            observer.update(professor, status, resumo)  # Passa resumo para os observadores