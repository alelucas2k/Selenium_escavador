"""
Padrão utilizado: Factory Method e Chain of Responsibility.
Explicação:
O HandlerFactory encapsula a criação da cadeia de handlers, que processa as etapas do scraping.
Isso permite que a criação e a composição dos handlers fiquem centralizadas, facilitando a extensão
ou modificação do fluxo de execução sem impactar o código cliente.
"""


from driver_handlers import OpenSiteHandler, SearchProfessorHandler, ClickProfileHandler, SaveResumeHandler

class HandlerFactory:
    @staticmethod
    def criar_cadeia():
        return OpenSiteHandler(SearchProfessorHandler(ClickProfileHandler(SaveResumeHandler())))
