import time

from repository.login.loginInterface import LoginInterface
from repository.login.loginReal import LoginReal


class LoginProxy(LoginInterface):
    def __init__(self):
        self.login_real = LoginReal()
        self.tentativas = {}  # Dicionário para armazenar tentativas de login

    def autenticar(self, email, senha):
        if email in self.tentativas:
            num_tentativas, ultimo_tempo = self.tentativas[email]
            if num_tentativas >= 3 and (time.time() - ultimo_tempo < 60):  # Bloqueia se 3 tentativas falharem em 1 min
                return {"status": "fail", "message": "Muitas tentativas. Aguarde um minuto."}

        resultado = self.login_real.autenticar(email, senha)

        if resultado["status"] == "fail":
            if email in self.tentativas:
                self.tentativas[email] = (self.tentativas[email][0] + 1, time.time())
            else:
                self.tentativas[email] = (1, time.time())
        else:
            self.tentativas.pop(email, None)  # Reseta tentativas se o login for bem-sucedido

        return resultado
