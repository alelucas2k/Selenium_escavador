class Observer:
    def update(self, professor, status):
        pass

class StatusLogger(Observer):
    def update(self, professor, status):
        print(f"[LOG] {professor} -> {status}")

class StatusDatabaseUpdater(Observer):
    def update(self, professor, status):
        from database import Database
        db = Database()
        db.executar("UPDATE professores SET status = ? WHERE nome = ?", (status, professor))

class Subject:
    def __init__(self):
        self._observers = []

    def adicionar_observador(self, observer):
        self._observers.append(observer)

    def notificar(self, professor, status):
        for observer in self._observers:
            observer.update(professor, status)
