"""
Padrão utilizado: Chain of Responsibility.
Explicação:
Cada handler (por exemplo, OpenSiteHandler, SearchProfessorHandler, ClickProfileHandler e SaveResumeHandler)
é responsável por uma etapa do fluxo de scraping.
O uso deste padrão permite que cada etapa delegue para a próxima, criando uma cadeia modular e facilmente extensível.
"""


import time
import subprocess
from selenium.webdriver.common.by import By
from observer import Subject, StatusLogger, StatusDatabaseUpdater
from gemini_summarizer import resumir_curriculo_gemini


class Handler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, context):
        if self.successor:
            return self.successor.handle(context)


class OpenSiteHandler(Handler):
    def handle(self, context):
        context['driver'].get("https://www.escavador.com/")
        time.sleep(5)
        print("Site aberto com sucesso.")
        return super().handle(context)


class SearchProfessorHandler(Handler):
    def __init__(self, successor=None):
        super().__init__(successor)
        self.subject = Subject()
        self.subject.adicionar_observador(StatusLogger())
        self.subject.adicionar_observador(StatusDatabaseUpdater())

    def handle(self, context):
        try:
            driver = context['driver']
            professor = context['professor']
            procurar = driver.find_element(By.XPATH,
                                           "/html/body/div/div/main/div[2]/main/div/section[1]/div[3]/form/div[1]/input")
            procurar.clear()
            procurar.send_keys(professor)
            time.sleep(2)
            clicar = driver.find_element(By.XPATH,
                                         "/html/body/div/div/main/div[2]/main/div/section[1]/div[3]/form/div[1]/button")
            clicar.click()
            time.sleep(5)
            print(f"Busca pelo professor {professor} realizada.")
            self.subject.notificar(professor, "encontrado")
            context['subject'] = self.subject
            return super().handle(context)
        except Exception:
            print(f"Erro ao buscar professor {professor}")
            self.subject.notificar(professor, "não encontrado")


class ClickProfileHandler(Handler):
    def handle(self, context):
        try:
            driver = context['driver']
            perfil = driver.find_element(By.XPATH, "/html/body/main/div[2]/section/div[2]/div[2]/a")
            perfil.click()
            time.sleep(5)
            print("Perfil clicado com sucesso.")
            return super().handle(context)
        except Exception as e:
            print(f"Erro ao clicar no perfil: {e}")
            context['subject'].notificar(context['professor'], "não encontrado")


class SaveResumeHandler(Handler):
    def handle(self, context):
        try:
            driver = context['driver']
            professor = context['professor']
            texto = driver.find_element(By.XPATH, "/html/body/main/div/section")
            div_text = texto.text
            nome_arquivo = f"curriculo_{professor.replace(' ', '_')}.txt"

            with open(nome_arquivo, "w", encoding="utf-8") as file:
                file.write(div_text)
            print(f"Currículo de {professor} salvo com sucesso em '{nome_arquivo}'!")

            # Gera o resumo utilizando a API Gemini
            resumo = resumir_curriculo_gemini(nome_arquivo)
            if resumo:
                print("Resumo gerado")
                context['subject'].notificar(professor, "resumo gerado", resumo)
            else:
                context['subject'].notificar(professor, "erro ao gerar resumo")
        except Exception as e:
            print(f"Erro ao salvar currículo: {e}")
            context['subject'].notificar(professor, "erro")
